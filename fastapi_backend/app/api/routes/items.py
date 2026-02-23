


# @router.post("/login/access-token")
# def login_access_token(
#     session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> Token:
#     """
#     OAuth2 compatible token login, get an access token for future requests
#     """
#     user = crud.authenticate(
#         session=session, email=form_data.username, password=form_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     return Token(
#         access_token = security.create_access_token(
#             user.id,expires_delta = access_token_expires
#         )
#     )