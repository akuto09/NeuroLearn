from flask import Blueprint, jsonify, session, request
from ai_engine import eeg_processing, recommendation_engine
from middleware.authentication import login_required

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/ai/metrics")
@login_required
def ai_metrics():
    key = f"user-{session.get('user_id')}"
    raw = eeg_processing.read_mental_state(key)
    result = recommendation_engine.evaluate(raw)
    return jsonify(result)


@api_bp.route("/ai/assistant", methods=["POST"])
@login_required
def ai_assistant():
    key = f"user-{session.get('user_id')}"
    raw = eeg_processing.read_mental_state(key)
    message = (request.get_json(silent=True) or {}).get("message", "")
    reply = recommendation_engine.assistant_reply(message, raw)
    return jsonify({"reply": reply})
