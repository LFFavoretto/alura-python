from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
from typing import List
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/estudantes/', response_model=schemas.Estudante)
def criar_estudante(estudante: schemas.EstudanteCreate, db: Session = Depends(get_db)):
    db_estudante = models.Estudante(
        nome = estudante.nome,
        email = estudante.email,
        perfil = models.Perfil(**estudante.perfil.dict())
    )
    db.add(db_estudante)
    db.commit()
    db.refresh(db_estudante)
    return db_estudante

@app.get('/estudantes/', response_model=List[schemas.Estudante])
def listar_estudantes(db: Session= Depends(get_db)):
    estudantes = db.query(models.Estudante).options(
        joinedload(models.Estudante.perfil)
    ).all()
    return estudantes

@app.post('/professores/', response_model=schemas.Professor)
def criar_professor(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    db_professor = models.Professor(
        nome = professor.nome,
        email = professor.email,
        perfil = models.Perfil(**professor.perfil.dict())
    )
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

@app.get('/professores/', response_model=List[schemas.Professor])
def listar_professores(db: Session= Depends(get_db)):
    professores = db.query(models.Professor).options(
        joinedload(models.Professor.perfil)
    ).all()
    return professores

@app.post('/disciplinas/', response_model=schemas.Disciplina)
def criar_disciplina(disciplina: schemas.DisciplinaCreate, db: Session = Depends(get_db)):
    professor = db.query(models.Professor).filter(models.Professor.id == disciplina.professor_id).first()
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    db_disciplina = models.Disciplina(
        nome = disciplina.nome,
        duracao = disciplina.duracao,
        professor_id = disciplina.professor_id,
    )
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

@app.get('/disciplinas/', response_model=List[schemas.Disciplina])
def listar_disciplinas(db: Session= Depends(get_db)):
    disciplinas = db.query(models.Disciplina).options(
        joinedload(models.Disciplina.professor)
    ).all()
    return disciplinas

@app.post('/matriculas/', response_model=schemas.Matricula)
def criar_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    estudante = db.query(models.Estudante).filter(models.Estudante.id == matricula.estudante_id).first()
    if estudante is None:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")

    disciplina = db.query(models.Disciplina).filter(models.Disciplina.id == matricula.disciplina_id).first()
    if disciplina is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    db_matricula = models.Matricula(
        estudante_id = matricula.estudante_id,
        disciplina_id = matricula.disciplina_id
    )
    db.add(db_matricula)
    db.commit()
    db.refresh(db_matricula)
    return db_matricula

@app.get('/matriculas/', response_model=List[schemas.Matricula])
def listar_matriculas(db: Session= Depends(get_db)):
    matriculas = db.query(models.Matricula).options(
        joinedload(models.Matricula.estudante),
        joinedload(models.Matricula.disciplina)
    ).all()
    return matriculas
