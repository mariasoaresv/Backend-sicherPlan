#cd backend
#python -m uvicorn main:app --reload

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

app = FastAPI(title="SicherPlan API")

@app.get("/")
def home():
    return {"status": "Backend do SicherPlan rodando"}


Base.metadata.create_all(bind=engine)

@app.post("/setores", response_model=schemas.SetorResponse)
def criar_setor(setor: schemas.SetorCreate, db: Session = Depends(get_db)):

    novo_setor = models.Setor(**setor.model_dump()) #Desempacota os campos do schema pro modelo
    
    db.add(novo_setor)
    db.commit()
    db.refresh(novo_setor)
    
    return novo_setor

@app.get("/setores", response_model=list[schemas.SetorResponse])
def listar_setores(db: Session = Depends(get_db)):
    setores = db.query(models.Setor).all()
    
    return setores

@app.get("/setores/{setor_id}", response_model=schemas.SetorResponse)
def buscar_setor_por_id(setor_id: int, db: Session = Depends(get_db)):
    setor = db.query(models.Setor).filter(models.Setor.id == setor_id).first()
    
    if not setor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Setor não encontrado"
        )
    
    return setor

@app.put("/setores/{setor_id}", response_model=schemas.SetorResponse)
def atualizar_setor_por_id(setor_id: int, dados_novos: schemas.SetorCreate, db: Session = Depends(get_db)):
    setor_banco = db.query(models.Setor).filter(models.Setor.id == setor_id).first()
    
    if not setor_banco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Setor não encontrado"
            )
    
    setor_banco.nome = dados_novos.nome
    setor_banco.descricao = dados_novos.descricao
    setor_banco.ativo = dados_novos.ativo
    
    db.commit()
    db.refresh(setor_banco)
    
    return setor_banco
    
    
@app.delete("/setores/{setor_id}")
def deletar_setor_por_id(setor_id: int, db: Session = Depends(get_db)):
    setor_banco = db.query(models.Setor).filter(models.Setor.id == setor_id).first()
    
    if not setor_banco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Setor não encontrado"
            )
      
    db.delete(setor_banco)
    db.commit() 
    
    return {"mensagem": "Setor deletado com sucesso"}