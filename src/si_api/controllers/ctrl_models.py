from dataclasses import dataclass


@dataclass
class LoginData:
    email: str
    password: str


@dataclass
class AuthData:
    access_token: str


@dataclass
class ErrorMsg:
    message: str
