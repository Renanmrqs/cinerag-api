from app.services.auth import add_token, read_tokens
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, security, HTTPException
from app.auth import pwd_context, generate_token, verify_token
from app.services.auth import get_users_by_identifier, get_users, create_register, update_register
from app.schemas import RegisterRequest, RegisterGoogle



# verificações de login e funcoes auxiliares
router = APIRouter()
security_rote = security.OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(security_rote)):
    blacklist = read_tokens(db, token)
    if not blacklist:
        user  = verify_token(token)
        return user
    raise HTTPException(status_code=401, detail='token expired')

def get_current_token(token: str = Depends(security_rote)):
    return token


#####
### rotas
# rota de puxar todos os usuarios
@router.get("/auth/users", tags=['auth'])
def read_all_users(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return get_users(db)


# #####registro de usuario
# ##faz a rota de criar o registro    
@router.post("/auth/register", tags=['auth'])
def post_register(register: RegisterRequest, db: Session = Depends(get_db)):
    try:
        password_criptografed = pwd_context.hash(register.password)
        create_register(db, register.email, register.username, password_criptografed)
        
        return {"message": f"user {register.username} registred"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f'{register.username} already in table')
    


# faz rota do usuario logar na aplicacao
@router.post("/auth/login", tags=['auth'])
def post_login(form_data: security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login_return = get_users_by_identifier(form_data.username, db)
    if not login_return:
        raise HTTPException(status_code=400, detail=f'{form_data.username} is not registred')
    
    password_corrrect = pwd_context.verify(form_data.password, login_return.password)
    if password_corrrect == False:
        raise HTTPException(status_code=400, detail=f'incorrect password, try again.')
    
    token = generate_token(form_data.username)
    
    return {"access_token": token, "token_type": "bearer", "user_id": login_return.id}


## rota de logout 

@router.post(f'/auth/logout', tags=['auth'])
def post_logout(token: str = Depends(get_current_token), user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        tk = add_token(db, token)
        return {'message': 'token add', 'data': tk}
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f'token already in table')

@router.patch(f'/auth/users/complete-profile', tags=['auth'])
def complete_profile(register: RegisterGoogle, email: str = Depends(get_current_user),  db: Session = Depends(get_db)):
    try:
        password_criptografed = pwd_context.hash(register.password)
        update_register(db, register.username, password_criptografed, email)
        return {"message": f"user {register.username} updated"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f'{register.username} not in table')