from dataclasses import dataclass
from typing import List


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


@dataclass
class Prediction:
    file: str
    prediction: List[str]


@dataclass
class Predictions:
    predictions: List[Prediction]
