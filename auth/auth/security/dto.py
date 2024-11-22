from datetime import datetime

from pydantic import BaseModel, field_validator


class UserRegistrationDTO(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def double(cls, username: str) -> str:
        if len(username) < 3 or len(username) > 20:
            raise ValueError("Username must be between 3 and 20 characters.")
        if not username.isalnum():
            raise ValueError("Username must be alphanumeric.")
        return username

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit.")
        if not any(c.isalpha() for c in password):
            raise ValueError("Password must contain at least one letter.")
        return password


class TokenDTO(BaseModel):
    access_token: str
    token_type: str
    expiration_date: datetime
