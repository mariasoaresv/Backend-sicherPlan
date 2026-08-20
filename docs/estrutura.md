# SicherPlan — Estrutura do Projeto

> **Stack:** Frontend → React + TypeScript (Vite) | Backend → Python / FastAPI | Banco → PostgreSQL | IA → Gemini API

---

## Visão Geral do Monorepo

```
SicherPlan/
├── docs/               ← Documentação do projeto
├── backend/            ← API REST (Python / FastAPI)
│   ├── main.py
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── .env.example
│   ├── alembic/        ← Migrations do banco
│   └── app/
│       ├── core/       ← Configuração, banco e segurança
│       ├── models/     ← Tabelas do banco (SQLAlchemy)
│       ├── schemas/    ← Validação de dados (Pydantic)
│       ├── routers/    ← Endpoints da API
│       └── services/   ← Regras de negócio
└── frontend/           ← Interface React + TypeScript
    ├── index.html
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/
        ├── types/      ← Interfaces TypeScript
        ├── contexts/   ← Estado global (Context API)
        ├── services/   ← Chamadas HTTP à API
        ├── hooks/      ← Custom Hooks
        ├── utils/      ← Funções utilitárias
        ├── styles/     ← CSS global e variáveis
        ├── pages/      ← Telas completas do sistema
        └── components/ ← Componentes reutilizáveis
```

---

## 📁 docs/

Documentação centralizada do projeto. Não contém código.

| Arquivo | Conteúdo |
|---|---|
| `SicherPlan_plan.md` | Planejamento geral: abas do sistema, relacionamentos, ordem de implementação |
| `estrutura.md` | Este arquivo — arquitetura de pastas e responsabilidades |

---

## 🐍 BACKEND

### `backend/` (raiz)

Arquivos de entrada e configuração do servidor Python.

| Arquivo | Função |
|---|---|
| `main.py` | Ponto de entrada do FastAPI — instancia o app, registra todos os routers e configura CORS |
| `requirements.txt` | Lista de dependências Python: FastAPI, SQLAlchemy, Alembic, Pydantic, python-jose, boto3, google-generativeai, python-docx |
| `alembic.ini` | Configuração do Alembic para gerenciar as migrations do PostgreSQL |
| `.env.example` | Modelo das variáveis de ambiente sem valores reais: `DATABASE_URL`, `GEMINI_API_KEY`, `SECRET_KEY`, `AWS_BUCKET_NAME` |

---

### `backend/alembic/`

Gerencia a evolução do schema do banco de dados sem perda de dados.

| Arquivo / Pasta | Função |
|---|---|
| `env.py` | Conecta o Alembic aos models SQLAlchemy para detectar mudanças automaticamente |
| `script.py.mako` | Template usado para gerar os arquivos de migration |
| `versions/` | Pasta que receberá cada migration gerada — um arquivo por alteração no banco |

> **Quem usa:** Toda vez que um model for criado ou alterado, o comando `alembic revision --autogenerate` gera um novo arquivo em `versions/` que é aplicado com `alembic upgrade head`.

---

### `backend/app/core/`

Configurações centrais compartilhadas por todo o backend.

| Arquivo | Função |
|---|---|
| `config.py` | Lê as variáveis do `.env` via Pydantic Settings e as expõe como objeto global — URL do banco, chave da API, etc. |
| `database.py` | Cria a engine do SQLAlchemy e a `SessionLocal`; fornece a função `get_db()` injetada nas rotas via `Depends()` |
| `security.py` | Funções de hash de senha (bcrypt), geração e validação de tokens JWT para autenticação e proteção de rotas |

---

### `backend/app/models/`

Cada arquivo define **uma tabela do banco de dados** usando SQLAlchemy ORM. Reflete os relacionamentos do planejamento.

| Arquivo | Tabela | Relacionamento principal |
|---|---|---|
| `setor.py` | `Setor` | 1 Setor → N Colaboradores |
| `funcao.py` | `Funcao` | 1 Função → N Colaboradores · N↔N EPIs obrigatórios |
| `colaborador.py` | `Colaborador` | Entidade central — tem Setor, Função, ASOs, Documentos, EPIs entregues |
| `epi.py` | `EPI` | 1 EPI → N CAs · N↔N Colaboradores (via Entrega) |
| `ca_epi.py` | `CA_EPI` | Certificado de Aprovação separado do EPI para suportar renovações |
| `entrega_epi.py` | `Entrega_EPI` | Tabela de junção Colaborador ↔ EPI com data de entrega e quantidade |
| `aso.py` | `ASO` | Atestado de Saúde Ocupacional — 1 Colaborador → N ASOs com data de vencimento |
| `certificado.py` | `Certificado` | NR 06, 12, 18, 35 — N↔N com Colaboradores via tabela de junção |
| `ordem_servico.py` | `OrdemServico` | N↔N com Colaboradores |
| `ficha_registro.py` | `FichaRegistro` | N↔N com Colaboradores |
| `documento_gerado.py` | `DocumentoGerado` | Registra todo PDF/DOCX gerado, URL no storage e vínculo com o colaborador |

---

### `backend/app/schemas/`

**Schemas Pydantic** — definem e validam o formato dos dados que entram e saem da API. Cada entidade tem schemas separados para criação, atualização e resposta. Nenhuma lógica de banco aqui.

| Arquivo | Schemas que conterá |
|---|---|
| `setor.py` | `SetorCreate`, `SetorResponse` |
| `funcao.py` | `FuncaoCreate`, `FuncaoResponse`, `MatrizEPIUpdate` |
| `colaborador.py` | `ColaboradorCreate`, `ColaboradorUpdate`, `ColaboradorResponse`, `ColaboradorDetalhe` |
| `epi.py` | `EPICreate`, `EPIResponse`, `CACreate`, `CAResponse` |
| `entrega.py` | `EntregaCreate`, `EntregaResponse`, `FichaEntregaData` |
| `aso.py` | `ASOCreate`, `ASOResponse` |
| `certificado.py` | `CertificadoCreate`, `CertificadoResponse` |
| `documento.py` | `DocumentoGeradoResponse`, `SolicitacaoDocumento` |

---

### `backend/app/routers/`

Cada arquivo é um **grupo de endpoints FastAPI** (`APIRouter`) montado no `main.py` com seu prefixo de URL.

| Arquivo | Prefixo | Responsabilidade |
|---|---|---|
| `setores.py` | `/setores` | CRUD de setores |
| `funcoes.py` | `/funcoes` | CRUD de funções + gestão de EPIs obrigatórios por função |
| `colaboradores.py` | `/colaboradores` | CRUD completo + upload de documentos + histórico de funções + listagem de EPIs pendentes |
| `epis.py` | `/epis` | CRUD de EPIs e CAs + upload do PDF do CA para storage |
| `entregas.py` | `/entregas` | Registro de entrega de EPI + geração de ficha digital |
| `asos.py` | `/asos` | Cadastro e listagem de ASOs com status de vencimento |
| `certificados.py` | `/certificados` | Vinculação de certificados a colaboradores |
| `documentos.py` | `/documentos` | Acionamento da geração de DOCX/PDF (NRs, Ordem de Serviço) |
| `agente_ia.py` | `/agente` | Recebe mensagem do usuário e retorna resposta do Gemini |
| `dashboard.py` | `/dashboard` | Queries prontas: ASOs a vencer, CAs a vencer, EPIs pendentes por setor |

---

### `backend/app/services/`

Camada de **regras de negócio** — lógica que não pertence ao router (HTTP) nem ao model (banco). Chamada pelos routers.

| Arquivo | Função |
|---|---|
| `validacao_ca.py` | Verifica vencimento do CA, aciona verificação 10 dias antes do prazo, integra com IA para validação automática do número do CA |
| `vencimentos.py` | Varredura geral de ASOs, CAs e certificados vencendo — alimenta o dashboard e gera alertas |
| `gerador_documentos.py` | Preenche templates `.docx` com dados reais do colaborador e gera o arquivo final (Ficha de EPI, NR 06, 12, 18, 35, Ordem de Serviço) |
| `agente_ia.py` | Orquestra as chamadas ao Gemini com contexto do sistema (dados de NRs, pendências do app, permissão de leitura/escrita) |
| `upload_arquivo.py` | Gerencia upload de PDFs (CAs, ASOs, certificados) para S3/MinIO e retorna a URL de acesso |

---

## ⚛️ FRONTEND

### `frontend/` (raiz)

Arquivos de configuração do projeto React.

| Arquivo | Função |
|---|---|
| `index.html` | Shell HTML — único arquivo HTML do SPA; monta o React no `<div id="root">` |
| `vite.config.ts` | Configuração do Vite: plugin React, proxy para `/api` apontando ao backend FastAPI |
| `tsconfig.json` | Regras TypeScript: strict mode, paths de importação curtos (`@/components/...`) |
| `.env.example` | Variáveis do frontend: `VITE_API_BASE_URL` |

---

### `frontend/src/types/`

**Interfaces TypeScript** de cada entidade — espelham os schemas do backend. Garantem tipagem forte em todo o frontend.

| Arquivo | Interfaces que conterá |
|---|---|
| `colaborador.ts` | `Colaborador`, `ColaboradorDetalhe`, `HistoricoFuncao` |
| `epi.ts` | `EPI`, `CA`, `StatusCA` |
| `setor.ts` | `Setor`, `Funcao`, `MatrizEPIObrigatorio` |
| `entrega.ts` | `Entrega`, `FichaEntregaItem` |
| `aso.ts` | `ASO`, `StatusVencimento` |
| `certificado.ts` | `Certificado`, `TipoCertificado` |
| `documento.ts` | `DocumentoGerado`, `TipoDocumento` |

---

### `frontend/src/contexts/`

Estado global da aplicação usando React Context API.

| Arquivo | Função |
|---|---|
| `AppContext.tsx` | Armazena setores/funções carregados globalmente (evita re-fetch), alertas de vencimento e configurações do app |
| `AuthContext.tsx` | Gerencia token JWT, dados do usuário logado, funções de login/logout e proteção de rotas privadas |

---

### `frontend/src/services/`

Cada arquivo encapsula as **chamadas HTTP** ao backend. Toda comunicação com a API passa por aqui.

| Arquivo | Chama os endpoints de |
|---|---|
| `api.ts` | Instância base do Axios com `baseURL` configurada e interceptor que injeta o token JWT em cada requisição |
| `colaboradoresService.ts` | `/colaboradores` — buscar, criar, editar, inativar, upload de documentos |
| `episService.ts` | `/epis` e `/epis/ca` — cadastrar EPIs, upload do PDF do CA |
| `setoresService.ts` | `/setores` e `/funcoes` — cadastrar estrutura organizacional |
| `entregasService.ts` | `/entregas` — registrar entrega, buscar histórico, gerar ficha |
| `asoService.ts` | `/asos` — criar e listar ASOs por colaborador |
| `documentosService.ts` | `/documentos` — solicitar geração e download de documentos |
| `agenteIAService.ts` | `/agente` — enviar mensagem e receber resposta do Gemini |

---

### `frontend/src/hooks/`

**Custom Hooks** que combinam chamadas de serviço com gerenciamento de estado local — reutilizáveis em qualquer página.

| Arquivo | Função |
|---|---|
| `useColaboradores.ts` | Busca, filtra por setor/função/status e pagina a lista de colaboradores |
| `useEpis.ts` | Busca EPIs já ordenados por proximidade de vencimento do CA |
| `useVencimentos.ts` | Retorna ASOs e CAs próximos do vencimento (janela de 30 dias) — usado no dashboard |
| `useDashboard.ts` | Agrega dados de `useVencimentos` e pendências em um único hook para a página de Dashboard |

---

### `frontend/src/utils/`

Funções puras e reutilizáveis — sem estado, sem chamadas HTTP.

| Arquivo | Função |
|---|---|
| `formatarData.ts` | Converte datas ISO (`2026-01-15`) para `DD/MM/YYYY` e vice-versa |
| `calcularVencimento.ts` | Calcula dias restantes até vencimento e retorna o status: `vencido`, `a_vencer`, `regular` |
| `validarCA.ts` | Valida formato do número do CA localmente antes de enviar ao backend |

---

### `frontend/src/styles/`

| Arquivo | Função |
|---|---|
| `variaveis.css` | Tokens de design: paleta de cores (verde floresta `#0f1f13`, verde SST `#16a34a`), espaçamentos, fontes, border-radius |
| `global.css` | Reset CSS, estilos base do `body`, sidebar, tipografia, classes utilitárias (`.aba-oculta`, `.btn-principal`) |

---

### `frontend/src/pages/`

Cada arquivo é a **tela completa** de uma aba do sistema. A página orquestra os sub-componentes e chama os hooks de dados.

| Arquivo | Aba do Sistema | Conteúdo principal |
|---|---|---|
| `Dashboard.tsx` | Visão Geral | Quadro de exames a vencer, quadro de CAs a vencer, filtro por setor |
| `Colaboradores.tsx` | Colaboradores | Tabela de funcionários + formulário de cadastro + detalhe com documentos |
| `EPIs.tsx` | Cadastro de EPIs | Tabela ordenada por vencimento + formulário + validação de CA com IA |
| `Setores.tsx` | Setores e Funções | Cadastro de setores/funções + matriz de EPIs obrigatórios por cargo |
| `Fornecimento.tsx` | Fornecimento / Entrega | Seleção de colaborador + pesquisa de EPI + geração de ficha |
| `GerarDocumentos.tsx` | Gerar Documentos | Calendário de geração + seletor de tipo de documento + download |
| `AgenteIA.tsx` | Agente de IA | Interface de chat + botão de relatório de pendências em DOCX |

---

### `frontend/src/components/`

Dois níveis: **componentes genéricos** (`ui/`) e **componentes de domínio** (subpastas por funcionalidade).

#### `components/ui/` — Kit de componentes reutilizáveis

| Arquivo | Função |
|---|---|
| `Sidebar.tsx` | Menu lateral fixo com navegação entre as abas — recebe a aba ativa e dispara troca de rota |
| `Tabela.tsx` | Componente genérico de tabela com suporte a ordenação e estado vazio |
| `Modal.tsx` | Modal reutilizável para confirmações, formulários de edição e alertas |
| `FormularioCampo.tsx` | Campo de formulário padrão com label, input/select e mensagem de erro |
| `BadgeStatus.tsx` | Badge colorido para exibir status: `Válido` (verde), `A Vencer` (amarelo), `Vencido` (vermelho) |
| `CardMetrica.tsx` | Card do dashboard com valor numérico, rótulo e ícone — reutilizado em Visão Geral |
| `UploadArquivo.tsx` | Botão de upload com indicador de status: `Não anexado` / `Anexado` |
| `BotaoPrincipal.tsx` | Botão primário com variantes de cor e estado de carregamento (spinner) |

#### `components/colaboradores/` — Componentes da aba Colaboradores

| Arquivo | Função |
|---|---|
| `FormColaborador.tsx` | Formulário de cadastro/edição com campos Nome, Matrícula, Setor (select), Função (select), Altura |
| `TabelaColaboradores.tsx` | Lista de funcionários com filtro Ativo/Inativo e paginação |
| `DetalheColaborador.tsx` | Painel lateral com todos os dados do colaborador selecionado |
| `DocumentosColaborador.tsx` | Lista de documentos obrigatórios com botão de upload e badge de status por documento |
| `HistoricoFuncoes.tsx` | Linha do tempo de mudanças de função com data e EPIs afetados |

#### `components/epis/` — Componentes da aba Cadastro de EPI

| Arquivo | Função |
|---|---|
| `FormEpi.tsx` | Formulário de cadastro de EPI com campos Nome, Grupo de Proteção, CA, Durabilidade |
| `TabelaEpis.tsx` | Lista de EPIs ordenada pela data de vencimento mais próxima primeiro |
| `ValidacaoCA.tsx` | Exibe o resultado da validação do CA (manual ou via IA) com data de vencimento calculada |
| `UploadCA.tsx` | Componente específico para upload do PDF do Certificado de Aprovação |

#### `components/setores/` — Componentes da aba Setores e Funções

| Arquivo | Função |
|---|---|
| `FormSetor.tsx` | Formulário para cadastrar novo setor e vincular funções a ele |
| `MatrizEpisObrigatorios.tsx` | Interface para selecionar quais EPIs já cadastrados são obrigatórios para cada função |
| `TreinamentosObrigatorios.tsx` | Cadastro de treinamentos/certificados obrigatórios por função com data de vencimento |

#### `components/fornecimento/` — Componentes da aba Fornecimento

| Arquivo | Função |
|---|---|
| `FormEntrega.tsx` | Seleção de colaborador + pesquisa de EPI por CA ou nome para registrar a entrega |
| `FichaEntrega.tsx` | Renderiza a ficha de entrega formatada com todos os EPIs entregues, datas e assinatura |
| `HistoricoEntregas.tsx` | Tabela com histórico de todas as entregas registradas |

#### `components/documentos/` — Componentes da aba Gerar Documentos

| Arquivo | Função |
|---|---|
| `SeletorDocumento.tsx` | Lista os tipos de documento disponíveis (NR 06, 12, 18, 35, Ficha EPI, Ordem de Serviço) |
| `CalendarioGeracao.tsx` | Seletor de data para definir a data de referência do documento gerado |

#### `components/dashboard/` — Componentes do Dashboard

| Arquivo | Função |
|---|---|
| `QuadroVencimentos.tsx` | Card com lista de colaboradores com exames/ASOs vencendo nos próximos 30 dias |
| `QuadroCAVencer.tsx` | Card com lista de EPIs cujo CA vence nos próximos 30 dias |
| `FiltroPorSetor.tsx` | Dropdown para filtrar todos os quadros do dashboard por setor |

#### `components/agente/` — Componentes da aba Agente de IA

| Arquivo | Função |
|---|---|
| `ChatAgente.tsx` | Interface de chat com histórico de mensagens, input de texto e resposta do Gemini com suporte a NRs |
| `RelatorioPendencias.tsx` | Botão que aciona a geração de um `.docx` com todas as pendências do sistema (CAs vencidos, documentos não anexados, ASOs vencidos) |
