# API Ordem de Serviço

## Visão Geral

API REST para criação de Ordens de Serviço desenvolvida utilizando princípios de arquitetura moderna, confiabilidade e observabilidade.

## Arquitetura

┌─────────────────────┐
│      FastAPI        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Controller      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       Service       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Repository      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
└──────────┬──────────┘
           │

## Configuração do Ambiente
1. Clonar Repositório
Shell
git clone <url-do-repositorio>
 
cd os-api
2. Criar Ambiente Virtual
Windows
Shell
python -m venv .venv
 
.venv\Scripts\activate
3. Instalar Dependências
Shell
pip install -r requirements.txt
4. Subir PostgreSQL
Shell
docker compose up -d

Verificar:

Shell
docker ps
5. Executar Migrations
Shell
alembic upgrade head
6. Executar API
Shell
uvicorn src.main:app --reload

### Documentação Swagger

Disponível em:

Plain Text
http://127.0.0.1:8000/docs
Health Check

Endpoint:

HTTP
GET /health

Resposta:

JSON
{
"status": "healthy"
}

### Criar Ordem de Serviço
Endpoint
HTTP
POST /ordens-servico
Headers
HTTP
Idempotency-Key
HTTP
X-Correlation-Id
Request
JSON
{
"solicitante_id": "123",
"descricao": "Troca de equipamento"
}
Response
JSON
{
"id": "uuid",
"solicitante_id": "123",
"descricao": "Troca de equipamento",
"status": "CRIADA"
}

### Validação de Solicitante

Antes da criação da Ordem de Serviço o sistema valida o solicitante através de um serviço externo (atualmente implementado como Fake Client).

Solicitantes válidos:

Plain Text
123
456
789
Problem Details

Erros seguem o padrão RFC 7807.

Exemplo
JSON
{
"type": "/errors/not-found",
"title": "Solicitante não encontrado",
"status": 404,
"detail": "O solicitante informado não existe"
}

### Idempotência

A API implementa controle de idempotência para evitar criação duplicada de Ordens de Serviço.

Primeira Requisição
HTTP
POST /ordens-servico
 
Idempotency-Key: os-001

Resultado:

JSON
{
"id": "abc123"
}
Segunda Requisição

Mesma chave:

HTTP
POST /ordens-servico
 
Idempotency-Key: os-001

Resultado:

JSON
{
"id": "abc123"
}

Nenhuma nova Ordem de Serviço é criada.

## Fluxo de Idempotência

flowchart TD

A[Request]

A --> B{Chave Existe?}

B -->|Sim| C[Retorna Resposta Salva]

B -->|Não| D[Criar Ordem]

D --> E[Salvar Chave]

E --> F[Retornar Resposta]

## Outbox Pattern

Após a criação da Ordem de Serviço, um evento é persistido na tabela de Outbox na mesma transação.

## Evento Criado
{
  "event_type": "ORDEM_SERVICO_CRIADA"
}

## Fluxo Outbox

flowchart TD

A[Criar Ordem]

A --> B[Criar Evento Outbox]

B --> C[Commit]

C --> D[Worker]

D --> E[Publicar Evento]

E --> F[Marcar Como Publicado]

## Worker

O Worker é responsável por:

Buscar eventos pendentes
Publicar eventos
Marcar eventos como publicados

## Status do Evento

Antes:
published = false

Após processamento:
published = true

## Observabilidade

Cada requisição recebe um Correlation ID.

Exemplo:
```http
X-Correlation-Id: b86124ad-b7cc-4bc6-a9ae-d7729d7410d4
```

## Propagação
```text
API
↓
Service
↓
Repository
↓
Outbox
↓
Worker
```

## Logs

```bash
[b86124ad-b7cc-4bc6-a9ae-d7729d7410d4]
INFO - Ordem criada
```

## Banco de Dados

```text
ordens_servico

idempotency_keys

outbox_events

alembic_version
```

## Testes

Executar Todos

```bash
pytest -v
```
Resultado Esperado
```bash
8 passed
```

### Testes Unitários

Cobertura:

Service Layer
Idempotência
Solicitante Inválido
Health Check

### Testes de Integração

Cobertura:

Criação de Ordem
Problem Details
Idempotência
Correlation ID

```bash
pytest -v
```

## Decisões Arquiteturais

### Repository Pattern

Objetivo:

Reduzir acoplamento
Facilitar testes
Isolar persistência

### Idempotência

Objetivo:

Evitar duplicidade causada por retries

### Outbox Pattern

Objetivo:

Garantir consistência entre banco de dados e eventos

### Correlation ID

Objetivo:

Rastreabilidade ponta a ponta

## Roadmap de Evolução

✅ JWT Authentication
✅ Retry no Worker
✅ Dead Letter Queue
✅ Grafana
✅ Kafka/RabbitMQ