import pytest

from models.models import (
    Case,
    Declension,
    Gender,
    LexicalEntry,
    Mutation,
    Noun,
    NounForm,
    Number,
    PartOfSpeech,
)
from parser_service.parser_service import (
    generate_all_noun_forms_from_db,
)

class FakeRepository:
    """
    Provides predictable data for service tests without using MySQL.
    """
    def __init__(self):
        self.entry = LexicalEntry(
            lemma="teach",
            definition="house",
            part_of_speech=PartOfSpeech.NOUN,
            noun_data=Noun(
                gender=Gender.MASCULINE,
                declension=Declension.SECOND,
                forms=[
                    NounForm(
                        surface_form="teach",
                        case=Case.NOMINATIVE,
                        number=Number.SINGULAR,
                        mutation=Mutation.NONE
                    ),
                    NounForm(
                        surface_form="a theach",
                        case=Case.VOCATIVE,
                        number=Number.SINGULAR,
                        mutation=Mutation.LENITION
                    ),
                    NounForm(
                        surface_form="tithe",
                        case=Case.NOMINATIVE,
                        number=Number.PLURAL,
                        mutation=Mutation.NONE
                    )
                ]
            )
        )
    def load_lexicon(self):
        return [self.entry]

    def get_lexical_entry(self, lemma):
        if lemma.lower() == self.entry.lemma.lower():
            return self.entry
        return None

@pytest.fixture
def repository():
    return FakeRepository()

def test_generate_all_noun_forms_from_db_valid(repository):
    result = generate_all_noun_forms_from_db(
        "teach",
        repository=repository
    )
    assert result["lemma"] == "teach"
    assert result["definition"] == "house"
    assert result["part_of_speech"] == "noun"
    assert result["gender"] == "masculine"
    assert result["declension"] == "second"
    assert any(
        form["case"] == "vocative"
        for form in result["forms"]
    )
    assert any(
        form["number"] == "plural"
        for form in result["forms"]
    )
    assert any(
        form["mutation"] == "lenition"
        for form in result["forms"]
    )

def test_generate_all_noun_forms_from_db_ignores_case(repository):
    result = generate_all_noun_forms_from_db(
        "TEACH",
        repository=repository
    )
    assert result["lemma"] == "teach"

def test_generate_all_noun_forms_from_db_removes_spaces(repository):
    result = generate_all_noun_forms_from_db(
        "  teach  ",
        repository=repository
    )
    assert result["lemma"] == "teach"

def test_generate_all_noun_forms_from_db_missing(repository):
    with pytest.raises(
        ValueError,
        match="not found in database"
    ):
        generate_all_noun_forms_from_db(
            "xyz",
            repository=repository
        )


def test_generate_all_noun_forms_from_db_empty(repository):
    with pytest.raises(
        ValueError,
        match="word cannot be empty"
    ):
        generate_all_noun_forms_from_db(
            "   ",
            repository=repository
        )

def test_generate_all_noun_forms_from_db_wrong_type(repository):
    with pytest.raises(
        TypeError,
        match="word must be a string"
    ):
        generate_all_noun_forms_from_db(
            123,
            repository=repository
        )
