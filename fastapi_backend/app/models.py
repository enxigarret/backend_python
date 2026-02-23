from sqlmodel import Field, Relationship, SQLModel


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"