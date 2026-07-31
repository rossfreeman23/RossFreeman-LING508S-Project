"""
Flask application for the Irish Noun Morphological Parser.

Flask receives browser and API requests, validates their basic
structure, and passes noun searches to the service layer.
"""

from typing import Callable

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
)

from parser_service.parser_service import (
    generate_all_noun_forms_from_db,
)

def create_app(
    parser_function: Callable[[str], dict] =
    generate_all_noun_forms_from_db
) -> Flask:
    """
    Create and configure the Flask application.

    A different parser function can be supplied during testing so
    Flask tests do not require MySQL.
    """
    flask_app = Flask(__name__)

    @flask_app.get("/")
    def index():
        """
        Display the Irish noun search form.
        """
        return render_template(
            "index.html",
            word="",
            result=None,
            error=None
        )

    @flask_app.post("/search")
    def search_noun():
        """
        Process an HTML form submission and display the result.
        """
        word = request.form.get("word", "")
        normalized_word = word.strip()
        if not normalized_word:
            return render_template(
                "index.html",
                word=word,
                result=None,
                error="word cannot be empty."
            ), 400
        try:
            result = parser_function(normalized_word)
        except ValueError as error:
            return render_template(
                "index.html",
                word=normalized_word,
                result=None,
                error=str(error)
            ), 404
        return render_template(
            "index.html",
            word=normalized_word,
            result=result,
            error=None
        ), 200
    @flask_app.post("/parse")
    def parse_noun():
        """
        Return a noun's complete paradigm as JSON.
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
        normalized_word = word.strip()
        if not normalized_word:
            return jsonify(
                {
                    "error": "word cannot be empty."
                }
            ), 400
        try:
            result = parser_function(normalized_word)
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
