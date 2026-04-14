from flask import jsonify, make_response, request, redirect


def health_check():
    return jsonify(
        {
            "success": True,
            "message": "LATAM PASS BR fake server is up",
            "protocols": ["SOAP/XML", "REST/JSON"],
        }
    ), 200


# ==========================================================
# SOAP/XML
# ==========================================================
def soap_accumulation_gateway():
    """
    Single SOAP gateway because the collection points both
    submit accumulation and accumulation status to the same path.

    We inspect the incoming XML body and return a static SOAP response.
    """
    raw_body = request.data.decode("utf-8", errors="ignore")

    # Very simple mock routing by XML content
    lowered = raw_body.lower()

    if "consultar" in lowered or "status" in lowered:
        xml_response = _soap_status_response()
    else:
        xml_response = _soap_submit_response()

    response = make_response(xml_response, 200)
    response.headers["Content-Type"] = "text/xml; charset=utf-8"
    return response


def _soap_submit_response() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:ebo="http://ebo.multiplusfidelidade.com.br/v1"
                  xmlns:ebs="http://ebs.multiplusfidelidade.com.br/v1">
  <soapenv:Header/>
  <soapenv:Body>
    <ebs:SubmeterLoteAcumuloOutput>
      <ebs:resposta>
        <ebo:codigo-retorno>0</ebo:codigo-retorno>
        <ebo:mensagem-retorno>Accumulation submitted successfully</ebo:mensagem-retorno>
        <ebo:id-externo-lote>mock-tx-123</ebo:id-externo-lote>
        <ebo:protocolo>mock-protocol-001</ebo:protocolo>
        <ebo:status-lote>RECEIVED</ebo:status-lote>
      </ebs:resposta>
    </ebs:SubmeterLoteAcumuloOutput>
  </soapenv:Body>
</soapenv:Envelope>"""


def _soap_status_response() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:ebo="http://ebo.multiplusfidelidade.com.br/v1"
                  xmlns:ebs="http://ebs.multiplusfidelidade.com.br/v1">
  <soapenv:Header/>
  <soapenv:Body>
    <ebs:ConsultarStatusLoteAcumuloOutput>
      <ebs:resposta>
        <ebo:codigo-retorno>0</ebo:codigo-retorno>
        <ebo:mensagem-retorno>Accumulation status retrieved successfully</ebo:mensagem-retorno>
        <ebo:id-externo-lote>mock-tx-123</ebo:id-externo-lote>
        <ebo:status-lote>PROCESSED</ebo:status-lote>
        <ebo:quantidade-itens>1</ebo:quantidade-itens>
      </ebs:resposta>
    </ebs:ConsultarStatusLoteAcumuloOutput>
  </soapenv:Body>
</soapenv:Envelope>"""


# ==========================================================
# REST/JSON
# ==========================================================
def oauth_authorize():
    """
    Mock login/authorize endpoint.
    Simulates redirect with auth code and state.
    """
    state = request.args.get("state", "mock-state")
    redirect_uri = request.args.get("redirect_uri", "http://localhost/callback")

    separator = "&" if "?" in redirect_uri else "?"
    callback_url = f"{redirect_uri}{separator}code=mock-auth-code&state={state}"

    return redirect(callback_url, code=302)


def oauth_token():
    """
    Mock exchange auth code for token.
    Accepts x-www-form-urlencoded.
    """
    grant_type = request.form.get("grant_type")
    code = request.form.get("code")

    return jsonify(
        {
            "access_token": "mock-access-token",
            "refresh_token": "mock-refresh-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": request.form.get("scope", "mock-scope"),
            "grant_type_received": grant_type,
            "code_received": code,
        }
    ), 200


def user_info():
    return jsonify(
        {
            "id": "mock-user-id",
            "email": "mock.user@rappi.com",
            "firstName": "Andres",
            "lastName": "Hernandez",
            "documentNumber": "123456789",
            "memberId": "123456789",
            "program": "LATAM_PASS",
            "status": "ACTIVE",
        }
    ), 200


def extended_user_info(member_id: str):
    return jsonify(
        {
            "memberId": member_id,
            "program": "latam-pass",
            "fullName": "Mock LATAM Pass Member",
            "email": "mock.user@rappi.com",
            "phone": "+550000000000",
            "country": "BR",
            "status": "ACTIVE",
            "availableMiles": 15000,
            "qualificationPoints": 500,
        }
    ), 200


def redeem(member_id: str):
    payload = request.get_json(silent=True) or []

    return jsonify(
        {
            "success": True,
            "message": "Redeem processed successfully",
            "memberId": member_id,
            "transactionsReceived": len(payload),
            "results": [
                {
                    "id": "tx-001",
                    "status": "APPROVED",
                    "authorizationCode": "mock-redeem-approval-001",
                }
            ],
        }
    ), 200


def accumulation_token():
    """
    Mock client_credentials token for accumulation REST flow.
    """
    return jsonify(
        {
            "access_token": "mock-accumulation-token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "accumulation",
        }
    ), 200


def create_accumulation(member_id: str):
    payload = request.get_json(silent=True) or {}

    return jsonify(
        {
            "success": True,
            "message": "Accumulation created successfully",
            "memberId": member_id,
            "transactionId": payload.get("transactionId", "mock-accumulation-tx-001"),
            "status": "RECEIVED",
        }
    ), 201


def status_accumulation(member_id: str, transaction_id: str):
    return jsonify(
        {
            "success": True,
            "memberId": member_id,
            "transactionId": transaction_id,
            "status": "PROCESSED",
            "message": "Accumulation status retrieved successfully",
        }
    ), 200
