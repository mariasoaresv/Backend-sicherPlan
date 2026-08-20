# SICHERPLAN - PROGRAMA DE SST

Aba Colaboradores

- Cadastro do funcionário:

| NOME | FUNÇÃO | SETOR | Trabalho em Altura  |
| --- | --- | --- | --- |
- Acesso ao funcionário onde mostra os dados cadastrados
- Acesso a lista total de funcionários
- Ativos / Inativos
- Documentos obrigatórios e botão de upload com status anexo / não anexado
- Análise de documento e validação automática da data de emissão
- Validação dos documentos
- Setor e função como itens de seleção, sendo possível de selecionar apenas opções já criadas
- Opção de mudança de função do funcionário, com histórico de funções e atualização dos EPIs obrigatórios
- EPIs pendentes para colaborador assim que cadastrado / alterado

Aba Cadastro de EPI

- Cadastro do EPI

| NOME DO EPI | GRUPO DE PROTEÇÃO | CA | STATUS |
| --- | --- | --- | --- |
| Ex: Luva Multitato Volk | Luva Multitato | Nº | Válido / Vencido |
- Validação do CA - lógica de vencimento
- Validação automática com IA
- Verificação automática novamente do CA 10 dias antes da data prevista de vencimento
- Equipamentos de proteção com ordem de vencimento - mais próximos de vencimento mostrados primeiro
- Importação do arquivo PDF do CA
- Durabilidade do EPI

Aba Setores e funções

- Cadastro setores e funções
- Cadastro EPIs obrigatórios para cada função - apenas EPIs já cadastrados
- Cadastro de treinamentos / documentos obrigatórios para função (linkar com anexo de documentos) e vencimentos dos documentos obrigatórios

Aba Fornecimento / Entrega

- Selecionar o colaborador
- Pesquisa do EPI por CA / Nome
- Gerar ficha de EPI com todos os EPIs fornecidos / Data de entrega / Layout próprio / Opção de gerar ficha em branco com os dados do colaborador

Aba AGENTE DE IA

→ Funcionalidades:

- Responder duvidas
- Embasamentos tecnicos de NRs
- Adicionar informações no proprio app
- Fixo na aba inicial
- Documentos pendentes (gera um .docx com todos as diretrizes do app que estão pendentes: documentos não anexados, CAs vencidos, certificados vencidos, ASOs vencidos)

Aba Gerar Documentos

Deve gerar o documento padrão com informações do colaborador já cadastrado, conforme campos do documento exigirem

Calendário com data para gerar

- Documentos padrões:
    - Certificado NR 06
    - Certificado NR 12
    - Certificado NR 18
    - Certificado NR 35
    - Ficha de EPI
    - Ordem de Serviço

DASHBOARD

- Quadro: exames a vencer com: Nome do colaborador / data de vencimento (atualizado 30 dias antes e persistente para vencidos)
- Quadro: EPIs com CA a vencer
- Filtro por setor

## Relacionamentos (modelagem)

- **Setor (1) → (N) Colaboradores** *(cada colaborador pertence a 1 setor)*
- **Função (1) → (N) Colaboradores** *(cada colaborador pertence a 1 função)*
- **Função (N) ↔ (N) EPIs obrigatórios** *(junção: Função_EPI_Obrigatório)*
- **Colaborador (N) ↔ (N) EPIs entregues** *(junção: Entrega_EPI)*
- **EPI (1) → (N) CAs** *(opcional, se separar CA em tabela CA_EPI)*
- **Colaborador (1) → (N) ASOs** *(ASO sempre vinculado a 1 único colaborador)*
- **Colaborador (N) ↔ (N) Certificados** *(junção: Colaborador_Certificado)*
- **Colaborador (N) ↔ (N) Fichas de registro** *(junção: Colaborador_FichaRegistro)*
- **Colaborador (N) ↔ (N) Ordens de Serviço** *(junção: Colaborador_OrdemServico)*

## Ordem de implementação (cadastro e controle)

1. **Criar o repositório e base do projeto**
    - Monorepo (recomendado) com `frontend/` e `backend/` (ou 2 repositórios separados).
    - Definir padrão de commits (Conventional Commits) e branches (`main` + `dev`).
2. **Ferramentas e stack sugeridas**
    - **Frontend**: React + TypeScript (Vite ou Next.js) + UI kit (MUI/Chakra) + React Hook Form + Zod (validação).
    - **Backend**: Python (FastAPI) + SQLAlchemy + Alembic (migrations).
    - **Banco**: PostgreSQL.
    - **Auth**: JWT (inicial) / OAuth (se precisar).
    - **Armazenamento de arquivos** (PDFs CA/ASO/certificados): S3 compatível (AWS S3/MinIO) ou storage do provedor.
    - **Agente IA** (opcional no MVP): Gemini via API (ou outro LLM) com funções/ferramentas bem limitadas (somente leitura no começo).
    - **DevOps**: Docker Compose (banco + backend + frontend), pre-commit, black/ruff (Python), eslint/prettier (TS).
3. **Desenhar as telas (UI) e navegação**
    - Layout base com menu: Colaboradores, EPIs, Setores/Funções, Entregas, Documentos, Dashboard.
    - Definir componentes padrão: tabela (lista), formulário (criar/editar), página de detalhe, modal de confirmação.
4. **Modelagem e migrations (banco)**
    - Criar tabelas mínimas do MVP:
        - Setor, Função, Colaborador
        - EPI, (opcional) CA_EPI
        - Entrega_EPI (junção)
        - ASO
        - Certificado + Colaborador_Certificado (junção)
        - Ficha_Registro + Colaborador_FichaRegistro (junção)
        - Ordem_Servico + Colaborador_OrdemServico (junção)
        - (se já usar) Função_EPI_Obrigatório
5. **CRUDs base (API + UI) — nesta ordem**
    1. Setores e Funções (cadastro mestre)
    2. Colaboradores (já obrigando selecionar 1 setor e 1 função)
    3. EPIs e CAs (com upload de PDF do CA)
    4. Matriz de EPI obrigatório por função
    5. Entregas de EPI (vincular colaborador ↔ EPI, registrar data/quantidade e gerar ficha)
    6. ASO (1 colaborador → N ASOs, com validação de vencimento)
    7. Certificados (N:N com colaboradores)
    8. Ordens de Serviço (N:N com colaboradores)
    9. Fichas de registro (N:N com colaboradores)
6. **Regras de negócio (implementar após cada CRUD)**
    - **Integridade**: colaborador sempre com setor+função; não excluir setor/função com colaboradores vinculados.
    - **Entrega de EPI**: só permitir entrega se EPI/CA estiver **válido** (se você separar CA).
    - **Pendências** (controle): ao cadastrar/alterar função do colaborador, recalcular lista de EPIs obrigatórios vs entregues.
    - **Vencimentos**:
        - CA a vencer/vencido (do catálogo de EPI/CA)
        - ASO a vencer/vencido
        - Certificados a vencer/vencido (se tiver validade)
    - **Histórico**: manter histórico de mudança de função (se você usar esse recurso).
7. **Dashboard (consultas prontas)**
    - Exames/ASO a vencer (30 dias).
    - CA de EPI a vencer (30 dias).
    - (opcional) EPIs obrigatórios pendentes por colaborador/função.
    - Filtro por setor.
8. **Geração de documentos (depois do controle estar firme)**
    - Templates (DOCX/PDF) para: Ficha de EPI, Certificados, Ordem de Serviço.
    - Preenchimento automático com dados do colaborador/entregas.
    - Armazenar PDF gerado e vincular ao(s) colaborador(es).
9. **Agente de IA (por último, como “camada” sobre o controle)**
    - Começar com **perguntas e respostas** (NRs, explicações) usando base fixa.
    - Depois permitir “relatórios de pendências” (somente leitura).
    - Só então permitir “criar/alterar cadastros” via IA, com confirmação obrigatória.