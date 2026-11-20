from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

class UsuarioCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    nome: str = Field(..., min_length=2, max_length=150)
    perfil: Literal["admin", "operador"] = "operador"

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str) -> str:
        email_limpo = v.strip().lower()
        if "@" not in email_limpo or "." not in email_limpo:
            raise ValueError("E-mail inválido.")
        return email_limpo

    @field_validator("nome")
    @classmethod
    def limpar_nome(cls, v: str) -> str:
        return v.strip()


class UsuarioUpdatePerfil(BaseModel):
    perfil: Literal["admin", "operador"]
    ativo: bool