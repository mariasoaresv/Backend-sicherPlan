import os
import re
from datetime import datetime
from docxtpl import DocxTemplate
from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend import models, schemas, main


def gerar_docx_certificado(dados: schemas.ColaboradorCertificadoCreate, db: Session) -> str:
    novo_registro = main.criar_colaborador_certificado(db=db, item=dados)

    colaborador = novo_registro.colaborador
    certificado_base = novo_registro.certificado
    nome_funcao = colaborador.funcao.nome if colaborador.funcao else "Não informada"
    
    contexto = {
        "nome_colaborador": colaborador.nome,
        "cpf": colaborador.cpf,
        "funcao_colaborador": nome_funcao,
        "data_conclusao": dados.data_conclusao.strftime("%d/%m/%Y"),
    }

    template_path = "backend/templates/modelo_certificado.docx"
    if not os.path.exists(template_path):
        raise HTTPException(status_code=500, detail="Modelo .docx não encontrado em backend/templates/")

    doc = DocxTemplate(template_path)
    doc.render(contexto)

    #deixa essa pasta pra armazenar os arquivos gerados pra teste mas ignorei no git
    pasta_saida = "backend/arquivos_gerados/certificados"
    os.makedirs(pasta_saida, exist_ok=True)
    
    nome_sanitizado = re.sub(r'[^a-zA-Z0-9_]', '_', colaborador.nome)
    caminho_saida = f"{pasta_saida}/Certificado_{nome_sanitizado}_{novo_registro.id}.docx"
    doc.save(caminho_saida)

    # não sei o caminho da url que vamos colocar no bd mas fica a função salva aqui
    # novo_registro.url_certificado = caminho_saida
    # db.commit()

    return caminho_saida