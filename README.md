# API Ordem de Serviço

## Visão Geral

API REST para criação de Ordens de Serviço desenvolvida utilizando princípios de arquitetura moderna, confiabilidade e observabilidade.

A solução foi construída para atender requisitos comuns de sistemas distribuídos, incluindo:

- Criação de Ordens de Serviço
- Idempotência
- Consistência transacional
- Integração com sistemas externos
- Processamento assíncrono
- Observabilidade
- Tratamento padronizado de erros
- Testes automatizados

## Objetivos da Solução

A API foi projetada para resolver os seguintes problemas:

### Evitar processamento duplicado

A mesma requisição pode ser enviada múltiplas vezes devido a retries, timeout ou reenvio manual.

Para isso foi implementada uma estratégia de Idempotência utilizando `Idempotency-Key`.

### Garantir consistência na publicação de eventos

Foi adotado o padrão Transactional Outbox.

### Fornecer rastreabilidade completa

Cada requisição possui um Correlation ID.

## Stack Tecnológica

- Python 3.15
- FastAPI
- Pydantic V2
- PostgreSQL
- SQLAlchemy 2
- Alembic
- Pytest
- Docker

## Estrutura do Projeto

```text
src/
├── api/
├── database/
├── exceptions/
├── integrations/
├── middlewares/
├── models/
├── observability/
├── repositories/
├── schemas/
├── services/
├── workers/
└── main.py
```

## Executar

```bash
docker compose up -d
alembic upgrade head
uvicorn src.main:app --reload
```

## Testes

```bash
pytest -v
```

## Funcionalidades Implementadas

- Repository Pattern
- Service Layer
- Idempotência
- Outbox Pattern
- Worker Assíncrono
- Correlation ID
- Problem Details (RFC7807)
- Testes Unitários
- Testes de Integração

## Resultado Final

✅ FastAPI
✅ PostgreSQL
✅ SQLAlchemy 2
✅ Alembic
✅ Idempotência
✅ Outbox Pattern
✅ Observabilidade
✅ Testes Automatizados
