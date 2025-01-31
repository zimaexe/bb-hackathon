from pydantic import BaseModel, EmailStr
from datetime import datetime


class Token(BaseModel):
    """
    Data model representing token response.

    Attributes:
        access_token (str): The access token string.
        expiration_date (datetime): The expiration datetime of the access token.
    """

    access_token: str
    token_type: str
    expiration_date: datetime


class TokenData(BaseModel):
    """
    TokenData is a Pydantic model used to represent the data contained in a token.
    Attributes:
        email (EmailStr): The email address associated with the token.
        scopes (list | str): The scopes or permissions associated with the token. This can be a list of scopes or a single scope as a string.
    """

    email: EmailStr
    scopes: list | str
