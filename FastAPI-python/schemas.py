from typing import List, Optional
from pydantic import BaseModel

class Perfil(BaseModel):
    id: int
    idade: int
    endereco: str

    class Config:
        from_attributes = True

class PerfilCreate(BaseModel):
    idade: int
    endereco: str

class Estudante(BaseModel):
    id: int
    email: str
    nome: str
    perfil: Optional[Perfil] = None

    class Config:
        from_attributes = True

class EstudanteCreate(BaseModel):
    nome: str
    email: str
    perfil: PerfilCreate

class Professor(BaseModel):
    id: int
    email: str
    nome: str
    perfil: Optional[Perfil] = None

    class Config:
        from_attributes = True

class ProfessorCreate(BaseModel):
    nome: str
    email: str
    perfil: PerfilCreate

class Disciplina(BaseModel):
    id: int
    nome: str
    duracao: str
    professor: Optional[Professor] = None

    class Config:
        from_attributes = True

class DisciplinaCreate(BaseModel):
    nome: str
    duracao: str
    professor_id: int

class Matricula(BaseModel):
    id: int
    estudante: Optional[Estudante] = None
    disciplina: Optional[Disciplina] = None

    class Config:
        from_attributes = True

class MatriculaCreate(BaseModel):
    estudante_id: int
    disciplina_id: int
