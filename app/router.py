from flask import Flask

from app.controllers.mock_latam_pass_br_controller import (
    health_check,
    soap_accumulation_gateway,
    oauth_authorize,
    oauth_token,
    user_info,
    extended_user_info,
    redeem,
    accumulation_token,
    create_accumulation,
    status_accumulation,
)


def create_app() -> Flask:
    app = Flask(__name__)

    configure_routes(app)
    return app


def configure_routes(app: Flask) -> None:
    # Health
    app.route("/health", methods=["GET"])(health_check)

    # SOAP/XML
    # Important:
    # In your collection both SOAP operations point to the same endpoint.
    # So we use one gateway controller and decide the mock response
    # by inspecting the XML body.
    app.route("/SubmeterLoteAcumuloAPISv1", methods=["POST"])(soap_accumulation_gateway)

    # REST/JSON
    app.route("/oauth/authorize", methods=["GET"])(oauth_authorize)
    app.route("/oauth/token", methods=["POST"])(oauth_token)
    app.route("/me", methods=["GET"])(user_info)
    app.route("/programs/latam-pass/members/<member_id>", methods=["GET"])(extended_user_info)
    app.route("/programs/LATAM_PASS/members/<member_id>/redeem", methods=["POST"])(redeem)
    app.route("/oauth/access-token", methods=["POST"])(accumulation_token)

    # Extra endpoints requested in the project scope
    app.route("/programs/LATAM_PASS/members/<member_id>/accumulation", methods=["POST"])(create_accumulation)
    app.route("/programs/LATAM_PASS/members/<member_id>/accumulation/<transaction_id>/status", methods=["GET"])(status_accumulation)
