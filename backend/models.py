from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, func, ForeignKey
from database import Base #Importa a base configurada no database.py

class Colaborador(Base):
    __tablename__ = "colaborador"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    data_nascimento = Column(Date)
    data_admissao = Column(Date, nullable=False)
    data_demissao = Column(Date)
    setor_id = Column(Integer, ForeignKey("setor.id"), nullable=False)
    funcao_id = Column(Integer, ForeignKey("funcao.id"), nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    atualizado_em = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    

class Setor(Base) :
    __tablename__ = "setor"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    atualizado_em = Column(DateTime, nullable=False, default=func.now(),onupdate=func.now())
    
    
class Funcao(Base) :
    __tablename__ = "funcao"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    setor_id = Column(Integer, ForeignKey("setor.id"), nullable=False)
    descricao = Column(String)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    atualizado_em = Column(DateTime, nullable=False, default=func.now(),onupdate=func.now())
    

class Epi(Base) :
    __tablename__ = "epi"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    grupo_protecao = Column(String, nullable=False)
    ca_numero = Column(String, nullable=False)
    data_validade_ca = Column(Date, nullable=False)
    durabilidade_dias = Column(Integer)
    url_pdf_ca = Column(String)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    atualizado_em = Column(DateTime, nullable=False, default=func.now(),onupdate=func.now())
    

class FuncaoEpiObrigatorio(Base) :
    __tablename__ = "funcao_epi_obrigatorio"
    id = Column(Integer, primary_key=True, index=True)
    funcao_id = Column(Integer, ForeignKey("funcao.id"), nullable=False)
    epi_id = Column(Integer, ForeignKey("epi.id"), nullable=False)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    

class HistoricoFuncao(Base) :
    __tablename__ = "historico_funcao"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"), nullable=False)
    funcao_id = Column(Integer, ForeignKey("funcao.id"), nullable=False)
    setor_id = Column(Integer, ForeignKey("setor.id"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    motivo_mudanca = Column(String)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    
    
class EntregaEpi(Base) :
    __tablename__ = "entrega_epi"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"), nullable=False)
    epi_id = Column(Integer, ForeignKey("epi.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    assinado = Column(Boolean, default=False)
    observacao = Column(String)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    atualizado_em = Column(DateTime, nullable=False, default=func.now(),onupdate=func.now())
    
    
class Aso(Base) :
    __tablename__ = "aso"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"), nullable=False)
    tipo = Column(String, nullable=False)
    data_emissao = Column(DateTime, nullable=False)
    data_vencimento = Column(DateTime, nullable=False)
    url_documento = Column(String)
    observacao = Column(String)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    atualizado_em = Column(DateTime, nullable=False, default=func.now(),onupdate=func.now())
    
    
class Certificado(Base) :
    __tablename__ = "certificado"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    nr_codigo = Column(String)
    carga_horaria = Column(Integer)
    validade_meses = Column(Integer)
    descricao = Column(String)
    criado_em = Column(DateTime, nullable=False, default=func.now())


class ColaboradorCertificado(Base) :
    __tablename__ = "colaborador_certificado"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"), nullable=False)
    certificado_id = Column(Integer, ForeignKey("certificado.id"), nullable=False)
    data_conclusao = Column(DateTime, nullable=False)
    data_vencimento = Column(DateTime)
    url_certificado = Column(String)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    
    
class OrdemServico(Base) :
    __tablename__ = "ordem_servico"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"), nullable=False)
    titulo = Column(String, nullable=False)
    data_emissao = Column(DateTime, nullable=False)
    assinado = Column(Boolean, default=False)
    url_documento = Column(String)
    criado_em = Column(DateTime, nullable=False, default=func.now())
    

class FichaRegistro(Base) :
    __tablename__ = "ficha_registro"
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey("colaborador.id"), nullable=False)
    tipo_documento = Column(String, nullable=False)
    url_documento = Column(String, nullable=False)
    validado = Column(Boolean, default=False)
    data_emissao = Column(DateTime, nullable=False)
    data_vencimento = Column(DateTime, nullable=False)
    criado_em = Column(DateTime, nullable=False, default=func.now())