from tests.conftest import client


def test_deve_criar_ordem():

    response = client.post(
        "/ordens-servico",
        headers={
            "Idempotency-Key": "integration-001"
        },
        json={
            "solicitante_id": "123",
            "descricao": "Teste integração"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "CRIADA"

    assert body["solicitante_id"] == "123"

def test_deve_retornar_404_para_solicitante_invalido():

    response = client.post(
        "/ordens-servico",
        headers={
            "Idempotency-Key": "integration-002"
        },
        json={
            "solicitante_id": "999",
            "descricao": "Teste"
        }
    )

    assert response.status_code == 404

    body = response.json()

    assert body["type"] == "/errors/not-found"

def test_nao_deve_criar_ordem_duplicada():

    payload = {
        "solicitante_id": "123",
        "descricao": "Teste Idempotência"
    }

    headers = {
        "Idempotency-Key": "integration-003"
    }

    response_1 = client.post(
        "/ordens-servico",
        headers=headers,
        json=payload
    )

    response_2 = client.post(
        "/ordens-servico",
        headers=headers,
        json=payload
    )

    assert response_1.json() == (
        response_2.json()
    )

def test_deve_retornar_correlation_id():

    response = client.post(
        "/ordens-servico",
        headers={
            "Idempotency-Key": "integration-004"
        },
        json={
            "solicitante_id": "123",
            "descricao": "Teste Correlation"
        }
    )

    assert (
        "x-correlation-id"
        in response.headers
    )