from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Estudante(Base):
    __tablename__= 'estudantes'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    perfil = relationship("Perfil", 
        back_populates = "estudante", 
        uselist = False,
        cascade = "all, delete-orphan"
    )
    disciplina = relationship("Disciplina",
        back_populates = "estudante",
        uselist = False,
        cascade = "all, delete-orphan")
    
    matricula = relationship("Matricula",
        back_populates = "estudante",
        uselist = False,
        cascade = "all, delete-orphan"
    )

class Professor(Base):
    __tablename__ = 'professores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    perfil = relationship("Perfil",
        back_populates = "professore",
        uselist = False,
        cascade = "all, delete-orphan"
    )
    disciplina = relationship("Disciplina",
        back_populates = "professore",
        uselist = False,
        cascade = "all, delete-orphan")

class Perfil(Base):
    __tablename__ = 'perfis'
    id = Column(Integer, primary_key=True, index=True)
    idade = Column(Integer)
    endereco = Column(String)
    estudante_id = Column(
        Integer,
        ForeignKey("estudantes.id"),
        unique=True
        )
    estudante = relationship(
        "Estudante",
        back_populates='perfil'
    )
    professor_id = Column(
        Integer,
        ForeignKey,
        unique=True
    )
    professor = relationship(
        "Professor",
        back_populates= "perfil"
    )

class Disciplina(Base):
    __tablename__ = 'disciplinas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    duracao = Column(String)
    professor_id = Column(
        Integer,
        ForeignKey,
        unique=True
    )
    professor = relationship(
        "Professor",
        back_populates= "disciplina"
    )

    estudante_id = Column(
        Integer,
        ForeignKey("estudantes.id"),
        unique=True
    )

    estudante = relationship(
        "Estudante",
        back_populates="disciplina"
    )

    matricula = relationship("Matricula",
        back_populates = "disciplina",
        uselist = False,
        cascade = "all, delete-orphan"
    )

class Matricula:
    id = Column(Integer, primary_key=True, index=True)
    estudante_id = Column(
        Integer,
        ForeignKey,
        unique=True
    )
    estudante = relationship(
        "Estudante",
        back_populates= "matricula"
    )

    disciplina_id = Column(
        Integer,
        ForeignKey,
        unique=True
    )

    disciplina = relationship(
        "Disciplina",
        back_populates= "matricula"
    )
