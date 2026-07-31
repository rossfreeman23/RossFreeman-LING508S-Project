# Tests for the Flask presentation layer.
# These tests use fake parser functions so they do not require MySQL.
# Database-backed behavior is tested separately in the end-to-end test.

import pytest
from app import create_app

def successful_parser(word):
    """
    Return predictable noun data without accessing MySQL.
    """
    return {
        "lemma": word.strip().lower(),
        "definition": "house",
        "part_of_speech": "noun",
        "gender": "masculine",
        "declension": "second",
        "forms": [
            {
                "surface_form": "teach",
                "case": "nominative",
                "number": "singular",
                "mutation": "none"
            },
            {
                "surface_form": "a theach",
                "case": "vocative",
                "number": "singular",
                "mutation": "lenition"
            }
        ]
    }

def missing_parser(word):
    """
    Simulate a noun that does not exist in the database.
    """
    raise ValueError(
        f"Noun '{word}' not found in database."
    )

@pytest.fixture
def client():
    """
    Create a Flask test client with a successful fake parser.
    """
    flask_app = create_app(
        parser_function=successful_parser
    )
    flask_app.config["TESTING"] = True
    return flask_app.test_client()

@pytest.fixture
def missing_client():
    """
    Create a Flask test client with a missing-entry parser.
    """
    flask_app = create_app(
        parser_function=missing_parser
    )
    flask_app.config["TESTING"] = True
    return flask_app.test_client()


# HTML form tests
# ==========================================================
def test_index_displays_search_form(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.content_type.startswith("text/html")
    page = response.get_data(as_text=True)
    assert "Irish Noun Morphological Parser" in page
    assert 'action="/search"' in page
    assert 'method="post"' in page
    assert 'name="word"' in page
    assert "Search" in page


def test_html_search_success(client):
    response = client.post(
        "/search",
        data={
            "word": "teach"
        }
    )
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Results for" in page
    assert "teach" in page
    assert "house" in page
    assert "Masculine" in page
    assert "Second" in page
    assert "Nominative" in page
    assert "Vocative" in page
    assert "a theach" in page


def test_html_search_removes_surrounding_spaces(client):
    response = client.post(
        "/search",
        data={
            "word": "  TEACH  "
        }
    )
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "teach" in page
    assert 'value="TEACH"' in page


def test_html_search_rejects_empty_word(client):
    response = client.post(
        "/search",
        data={
            "word": "   "
        }
    )
    assert response.status_code == 400
    page = response.get_data(as_text=True)
    assert "Search error" in page
    assert "word cannot be empty." in page


def test_html_search_handles_missing_noun(missing_client):
    response = missing_client.post(
        "/search",
        data={
            "word": "xyz"
        }
    )
    assert response.status_code == 404
    page = response.get_data(as_text=True)
    assert "Search error" in page
    assert "Noun &#39;xyz&#39; not found in database." in page


# JSON API tests
# ==========================================================
def test_parse_noun_success(client):
    response = client.post(
        "/parse",
        json={
            "word": "teach"
        }
    )
    assert response.status_code == 200
    assert response.content_type.startswith("application/json")
    response_data = response.get_json()
    assert response_data["lemma"] == "teach"
    assert response_data["definition"] == "house"
    assert response_data["part_of_speech"] == "noun"
    assert response_data["gender"] == "masculine"
    assert response_data["declension"] == "second"
    assert len(response_data["forms"]) == 2
    assert response_data["forms"][0] == {
        "surface_form": "teach",
        "case": "nominative",
        "number": "singular",
        "mutation": "none"
    }


def test_parse_noun_missing_from_database(missing_client):
    response = missing_client.post(
        "/parse",
        json={
            "word": "xyz"
        }
    )
    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Noun 'xyz' not found in database."
    }

def test_parse_rejects_missing_json(client):
    response = client.post("/parse")
    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Request body must be a JSON object."
    }

def test_parse_rejects_missing_word(client):
    response = client.post(
        "/parse",
        json={}
    )
    assert response.status_code == 400
    assert response.get_json() == {
        "error": "word must be a string."
    }

def test_parse_rejects_empty_word(client):
    response = client.post(
        "/parse",
        json={
            "word": "   "
        }
    )
    assert response.status_code == 400
    assert response.get_json() == {
        "error": "word cannot be empty."
    }

def test_parse_rejects_non_string_word(client):
    response = client.post(
        "/parse",
        json={
            "word": 123
        }
    )
    assert response.status_code == 400
    assert response.get_json() == {
        "error": "word must be a string."
    }
