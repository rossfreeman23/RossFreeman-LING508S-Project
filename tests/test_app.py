import pytest
from app import create_app

def successful_parser(word):
    """
    Return predictable parser data without accessing MySQL.
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

@pytest.fixture
def client():
    flask_app = create_app(
        parser_function=successful_parser
    )
    flask_app.config["TESTING"] = True
    return flask_app.test_client()

def test_index_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    response_data = response.get_json()
    assert (
        response_data["application"]
        == "Irish Noun Morphological Parser"
    )
    assert response_data["endpoint"] == "/parse"
    assert response_data["method"] == "POST"


def test_parse_noun_success(client):
    response = client.post(
        "/parse",
        json={
            "word": "teach"
        }
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["lemma"] == "teach"
    assert response_data["definition"] == "house"
    assert response_data["gender"] == "masculine"
    assert response_data["declension"] == "second"
    assert len(response_data["forms"]) == 2

def test_parse_noun_missing_from_database():
    def missing_parser(word):
        raise ValueError(
            f"Noun '{word}' not found in database."
        )
    flask_app = create_app(
        parser_function=missing_parser
    )
    flask_app.config["TESTING"] = True
    client = flask_app.test_client()
    response = client.post(
        "/parse",
        json={
            "word": "xyz"
        }
    )
    assert response.status_code == 404
    assert (
        response.get_json()["error"]
        == "Noun 'xyz' not found in database."
    )

def test_parse_rejects_missing_json(client):
    response = client.post("/parse")
    assert response.status_code == 400
    assert (
        response.get_json()["error"]
        == "Request body must be a JSON object."
    )

def test_parse_rejects_missing_word(client):
    response = client.post(
        "/parse",
        json={}
    )
    assert response.status_code == 400
    assert (
        response.get_json()["error"]
        == "word must be a string."
    )

def test_parse_rejects_empty_word(client):
    response = client.post(
        "/parse",
        json={
            "word": "   "
        }
    )
    assert response.status_code == 400
    assert (
        response.get_json()["error"]
        == "word cannot be empty."
    )

def test_parse_rejects_non_string_word(client):
    response = client.post(
        "/parse",
        json={
            "word": 123
        }
    )
    assert response.status_code == 400
    assert (
        response.get_json()["error"]
        == "word must be a string."
    )
