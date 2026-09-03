import os
import re
from docxtpl import DocxTemplate
from sqlalchemy.orm import Session
from fastapi import HTTPException

import schemas

def gerar_docx_certificado(dados: schemas.CertificadoDocumentoDados, db: Session = None) -> str:
    # função usada apenas para gerar o .docx, descomentar quando rodar
    # novo_registro = main.criar_colaborador_certificado(db=db, item=dados)
    # colaborador = novo_registro.colaborador
    # certificado_base = novo_registro.certificado
    # nome_funcao = colaborador.funcao.nome if colaborador.funcao else "Não informada"

    contexto = {
        "nome_colaborador": dados.nome_colaborador,
        "cpf": dados.cpf,
        "funcao_colaborador": dados.funcao_colaborador,
        "data_conclusao": dados.data_conclusao.strftime("%d/%m/%Y") if hasattr(dados.data_conclusao, "strftime") else dados.data_conclusao,
    }

    template_path = "templates/modelo_certificado.docx"
    if not os.path.exists(template_path):
        raise HTTPException(status_code=500, detail="Modelo .docx não encontrado em backend/templates/")

    doc = DocxTemplate(template_path)
    doc.render(contexto)

    #deixa essa pasta pra armazenar os arquivos gerados pra teste mas ignorei no git
    # excluir depois de testar
    pasta_saida = "arquivos_gerados/certificados"
    os.makedirs(pasta_saida, exist_ok=True)
    
    nome_sanitizado = re.sub(r'[^a-zA-Z0-9_]', '_', dados.nome_colaborador)
    caminho_saida = f"{pasta_saida}/Certificado_{nome_sanitizado}.docx"
    doc.save(caminho_saida)

    # não sei o caminho da url que vamos colocar no bd mas fica a função salva aqui
    # novo_registro.url_certificado = caminho_saida
    # db.commit()

    return caminho_saida