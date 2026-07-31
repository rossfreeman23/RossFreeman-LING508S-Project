#this app.py file initiates flask (a microframework allowing simple URL routing & request handling
#Here, flask's main job is to receive an HTTP request (i.e. user query) and hand it off to the Service Layer
from typing import Callable
from flask import Flask, jsonify, request
from parser_service.parser_service import (
    generate_all_noun_forms_from_db,
)

def create_app(
    parser_function: Callable[[str], dict] =
    generate_all_noun_forms_from_db
) -> Flask:
    """
    Create and configure the Flask application.
    A different parser function can be supplied during testing so the
    Flask tests do not require MySQL.
    """
    flask_app = Flask(__name__)

    @flask_app.get("/")
    def index():
        """
        Describe the API and its primary endpoint.
        """
        return jsonify(
            {
                "application": "Irish Noun Morphological Parser",
                "endpoint": "/parse",
                "method": "POST",
                "request_format": {
                    "word": "Irish noun"
                }
            }
        )

    @flask_app.post("/parse")
    def parse_noun():
        """
        Retrieve the complete morphological paradigm for an Irish noun.
        """
        request_data = request.get_json(silent=True)
        if not isinstance(request_data, dict):
            return jsonify(
                {
                    "error": "Request body must be a JSON object."
                }
            ), 400
        word = request_data.get("word")
        if not isinstance(word, str):
            return jsonify(
                {
                    "error": "word must be a string."
                }
            ), 400
        if not word.strip():
            return jsonify(
                {
                    "error": "word cannot be empty."
                }
            ), 400
        try:
            result = parser_function(word)
        except ValueError as error:
            return jsonify(
                {
                    "error": str(error)
                }
            ), 404
        return jsonify(result), 200
    return flask_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
