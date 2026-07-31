# NOTE: Tests Python classes only (not the database or service layer).
# These tests verify that the application's data model (classes)
# behaves correctly before any database or service logic is involved.

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
    Word,
)

# Enumeration tests
@pytest.mark.parametrize(
    ("member", "expected_name", "expected_value"),
    [
        (Gender.MASCULINE, "MASCULINE", 1),
        (Gender.FEMININE, "FEMININE", 2),

        (Case.NOMINATIVE, "NOMINATIVE", 1),
        (Case.GENITIVE, "GENITIVE", 2),
        (Case.DATIVE, "DATIVE", 3),
        (Case.VOCATIVE, "VOCATIVE", 4),

        (Number.SINGULAR, "SINGULAR", 1),
        (Number.PLURAL, "PLURAL", 2),

        (Declension.FIRST, "FIRST", 1),
        (Declension.SECOND, "SECOND", 2),
        (Declension.THIRD, "THIRD", 3),
        (Declension.FOURTH, "FOURTH", 4),
        (Declension.FIFTH, "FIFTH", 5),

        (Mutation.NONE, "NONE", 1),
        (Mutation.LENITION, "LENITION", 2),
        (Mutation.ECLIPSIS, "ECLIPSIS", 3),

        (PartOfSpeech.NOUN, "NOUN", 1),
        (PartOfSpeech.VERB, "VERB", 2),
        (PartOfSpeech.ADJECTIVE, "ADJECTIVE", 3),
    ]
)
def test_enumeration_member(
    member,
    expected_name,
    expected_value
):
    assert member.name == expected_name
    assert member.value == expected_value

# NounForm tests
def test_noun_form_creation():
    noun_form = NounForm(
        surface_form="teach",
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    assert noun_form.surface_form == "teach"
    assert noun_form.case is Case.NOMINATIVE
    assert noun_form.number is Number.SINGULAR
    assert noun_form.mutation is Mutation.NONE

@pytest.mark.parametrize(
    "arguments",
    [
        {
            "surface_form": 123,
            "case": Case.NOMINATIVE,
            "number": Number.SINGULAR,
            "mutation": Mutation.NONE
        },
        {
            "surface_form": "teach",
            "case": "NOMINATIVE",
            "number": Number.SINGULAR,
            "mutation": Mutation.NONE
        },
        {
            "surface_form": "teach",
            "case": Case.NOMINATIVE,
            "number": "SINGULAR",
            "mutation": Mutation.NONE
        },
        {
            "surface_form": "teach",
            "case": Case.NOMINATIVE,
            "number": Number.SINGULAR,
            "mutation": "NONE"
        }
    ]
)
def test_noun_form_rejects_invalid_attributes(arguments):
    with pytest.raises(TypeError):
        NounForm(**arguments)

# Noun tests
def test_noun_creation():
    nominative_form = NounForm(
        surface_form="teach",
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    genitive_form = NounForm(
        surface_form="tí",
        case=Case.GENITIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.SECOND,
        forms=[
            nominative_form,
            genitive_form
        ]
    )
    assert noun.gender is Gender.MASCULINE
    assert noun.declension is Declension.SECOND
    assert len(noun.forms) == 2
    assert noun.forms[0] is nominative_form
    assert noun.forms[1] is genitive_form

@pytest.mark.parametrize(
    "arguments",
    [
        {
            "gender": "MASCULINE",
            "declension": Declension.SECOND,
            "forms": []
        },
        {
            "gender": Gender.MASCULINE,
            "declension": "SECOND",
            "forms": []
        },
        {
            "gender": Gender.MASCULINE,
            "declension": Declension.SECOND,
            "forms": "not a list"
        },
        {
            "gender": Gender.MASCULINE,
            "declension": Declension.SECOND,
            "forms": ["not a NounForm"]
        }
    ]
)
def test_noun_rejects_invalid_attributes(arguments):
    with pytest.raises(TypeError):
        Noun(**arguments)


# LexicalEntry tests
def test_lexical_entry_creation():
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.SECOND,
        forms=[]
    )
    entry = LexicalEntry(
        lemma="teach",
        definition="house",
        part_of_speech=PartOfSpeech.NOUN,
        noun_data=noun
    )
    assert entry.lemma == "teach"
    assert entry.definition == "house"
    assert entry.part_of_speech is PartOfSpeech.NOUN
    assert entry.noun_data is noun

def test_lexical_entry_allows_no_noun_data():
    entry = LexicalEntry(
        lemma="example",
        definition="example definition",
        part_of_speech=PartOfSpeech.ADJECTIVE,
        noun_data=None
    )
    assert entry.noun_data is None

@pytest.mark.parametrize(
    "arguments",
    [
        {
            "lemma": 123,
            "definition": "house",
            "part_of_speech": PartOfSpeech.NOUN,
            "noun_data": None
        },
        {
            "lemma": "teach",
            "definition": 123,
            "part_of_speech": PartOfSpeech.NOUN,
            "noun_data": None
        },
        {
            "lemma": "teach",
            "definition": "house",
            "part_of_speech": "NOUN",
            "noun_data": None
        },
        {
            "lemma": "teach",
            "definition": "house",
            "part_of_speech": PartOfSpeech.NOUN,
            "noun_data": "not a Noun"
        }
    ]
)
def test_lexical_entry_rejects_invalid_attributes(arguments):
    with pytest.raises(TypeError):
        LexicalEntry(**arguments)


# Word tests
def test_word_creation():
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.SECOND,
        forms=[]
    )
    entry = LexicalEntry(
        lemma="teach",
        definition="house",
        part_of_speech=PartOfSpeech.NOUN,
        noun_data=noun
    )
    word = Word(
        surface_form="teach",
        entries=[entry]
    )
    assert word.surface_form == "teach"
    assert len(word.entries) == 1
    assert word.entries[0] is entry

def test_word_supports_multiple_entries():
    first_entry = LexicalEntry(
        lemma="example",
        definition="first analysis",
        part_of_speech=PartOfSpeech.NOUN,
        noun_data=None
    )
    second_entry = LexicalEntry(
        lemma="example",
        definition="second analysis",
        part_of_speech=PartOfSpeech.ADJECTIVE,
        noun_data=None
    )
    word = Word(
        surface_form="example",
        entries=[
            first_entry,
            second_entry
        ]
    )
    assert len(word.entries) == 2
    assert word.entries[0] is first_entry
    assert word.entries[1] is second_entry

@pytest.mark.parametrize(
    "arguments",
    [
        {
            "surface_form": 123,
            "entries": []
        },
        {
            "surface_form": "teach",
            "entries": "not a list"
        },
        {
            "surface_form": "teach",
            "entries": ["not a LexicalEntry"]
        }
    ]
)
def test_word_rejects_invalid_attributes(arguments):
    with pytest.raises(TypeError):
        Word(**arguments)
