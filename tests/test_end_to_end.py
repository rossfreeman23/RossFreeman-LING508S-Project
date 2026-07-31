# End-to-end tests for the Irish Noun Morphological Parser.
# These tests use the real Flask application, parser service, MysqlRepository, and grammar_db database.
# To work: MySQL must be running, the database must be initialized, and connection environment variables must be configured before these tests are executed.

import pytest
from app import app as flask_app

@pytest.fixture
def client():
    """
   Create a test client for the real Flask application.
    Unlike test_app.py, no fake parser function is injected.
    """
    flask_app.config["TESTING"] = True
    return flask_app.test_client()

def test_parse_noun_end_to_end(client):
    """
    Verify the complete JSON API request path:
    Flask API -> service -> repository -> MySQL -> response
    """
    response = client.post(
        "/parse",
        json={
            "word": "teach"
        }
    )
    assert response.status_code == 200
    assert response.content_type.startswith(
        "application/json"
    )
    result = response.get_json()
    assert result["lemma"] == "teach"
    assert result["definition"] == "house"
    assert result["part_of_speech"] == "noun"
    assert result["gender"] == "masculine"
    assert result["declension"] == "second"
    assert len(result["forms"]) == 8
    assert any(
        form == {
            "surface_form": "teach",
            "case": "nominative",
            "number": "singular",
            "mutation": "none"
        }
        for form in result["forms"]
    )
    assert any(
        form == {
            "surface_form": "tí",
            "case": "genitive",
            "number": "singular",
            "mutation": "none"
        }
        for form in result["forms"]
    )
    assert any(
        form == {
            "surface_form": "a theach",
            "case": "vocative",
            "number": "singular",
            "mutation": "lenition"
        }
        for form in result["forms"]
    )

def test_html_search_end_to_end(client):
    """
    Verify the complete HTML form request path:
    Form submission -> service -> repository -> MySQL -> HTML
    """
    response = client.post(
        "/search",
        data={
            "word": "madra"
        }
    )
    assert response.status_code == 200
    assert response.content_type.startswith("text/html")
    page = response.get_data(as_text=True)
    assert "Results for" in page
    assert "madra" in page
    assert "dog" in page
    assert "Masculine" in page
    assert "Fourth" in page
    assert "madraí" in page
    assert "a mhadra" in page
