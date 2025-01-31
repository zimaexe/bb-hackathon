from pydantic import BaseModel
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

class TokenInfo(BaseModel):
    email: