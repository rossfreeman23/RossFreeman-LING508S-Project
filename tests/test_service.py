import pytest
from services.parser_service import generate_all_noun_forms_from_db
def test_generate_all_noun_forms_from_db_valid():
    result = generate_all_noun_forms_from_db("bád")
    assert result["lemma"] == "bád"
    assert result["definition"] == "boat"
    assert result["gender"] == "masculine"
    assert result["declension"] == "first"
    assert any(f["case"] == "vocative" for f in result["forms"])
    assert any(f["number"] == "plural" for f in result["forms"])
def test_generate_all_noun_forms_from_db_invalid():
    with pytest.raises(ValueError):
        generate_all_noun_forms_from_db("xyz")
