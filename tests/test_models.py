# NOTE: Tests Python classes only (not the database or service layer).
# These tests verify that the application's data model (classes)
# behaves correctly before any database or service logic is involved.

# Import pytest for unit testing.
import pytest

# Import the project's model classes and enumerations.
from models.models import (
    Word,
    LexicalEntry,
    Noun,
    NounForm,
    Gender,
    Declension,
    Case,
    Number,
    Mutation,
    PartOfSpeech
)


# Enumeration Tests
def test_gender_enum():
    assert Gender.MASCULINE.name == "MASCULINE"
    assert Gender.FEMININE.name == "FEMININE"

def test_case_enum():
    assert Case.NOMINATIVE.name == "NOMINATIVE"
    assert Case.GENITIVE.name == "GENITIVE"
    assert Case.DATIVE.name == "DATIVE"
    assert Case.VOCATIVE.name == "VOCATIVE"

def test_number_enum():
    assert Number.SINGULAR.name == "SINGULAR"
    assert Number.PLURAL.name == "PLURAL"

def test_declension_enum():
    assert Declension.FIRST.name == "FIRST"
    assert Declension.FIFTH.name == "FIFTH"

def test_mutation_enum():
    assert Mutation.NONE.name == "NONE"
    assert Mutation.LENITION.name == "LENITION"
    assert Mutation.ECLIPSIS.name == "ECLIPSIS"

def test_part_of_speech_enum():
    assert PartOfSpeech.NOUN.name == "NOUN"


# The remaining tests use representative Irish nouns.
# They verify the model classes and do not test the database.

# NounForm Test
def test_noun_form_creation():
    noun_form = NounForm(
        surface_form="teach",
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
        )
    assert noun_form.surface_form == "teach"
    assert noun_form.case == Case.NOMINATIVE
    assert noun_form.number == Number.SINGULAR
    assert noun_form.mutation == Mutation.NONE

def test_noun_form_invalid_case():
    with pytest.raises(TypeError):
        NounForm(
            surface_form="teach",
            case="NOMINATIVE",
            number=Number.SINGULAR,
            mutation=Mutation.NONE
        )

def test_noun_form_invalid_number():
    with pytest.raises(TypeError):
        NounForm(
            surface_form="teach",
            case=Case.NOMINATIVE,
            number="SINGULAR",
            mutation=Mutation.NONE
        )

# Noun Tests
def test_noun_creation():
    form1 = NounForm(
        surface_form="teach",
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    form2 = NounForm(
        surface_form="tithe",
        case=Case.GENITIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.FIRST,
        forms=[form1, form2]
    )
    assert noun.gender == Gender.MASCULINE
    assert noun.declension == Declension.FIRST
    assert len(noun.forms) == 2
    assert noun.forms[0].surface_form == "teach"
    assert noun.forms[1].surface_form == "tithe"

def test_noun_rejects_invalid_forms():
    with pytest.raises(TypeError):
        Noun(
            gender=Gender.MASCULINE,
            declension=Declension.FIRST,
            forms=["not a noun form"]
        )

# LexicalEntry Tests
def test_lexical_entry_creation():
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.FIRST,
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
    assert entry.part_of_speech == PartOfSpeech.NOUN
    assert entry.noun_data == noun
def test_lexical_entry_rejects_invalid_pos():
    with pytest.raises(TypeError):
        LexicalEntry(
            lemma="teach",
            definition="house",
            part_of_speech="noun",
            noun_data=None
        )
def test_lexical_entry_rejects_invalid_noun():
    with pytest.raises(TypeError):
        LexicalEntry(
            lemma="teach",
            definition="house",
            part_of_speech=PartOfSpeech.NOUN,
            noun_data="not a noun"
        )

# Word Tests
def test_word_creation():
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.FIRST,
        forms=[]
    )
    entry1 = LexicalEntry(
        lemma="teach",
        definition="house",
        part_of_speech=PartOfSpeech.NOUN,
        noun_data=noun
    )
    entry2 = LexicalEntry(
        lemma="madra",
        definition="dog",
        part_of_speech=PartOfSpeech.NOUN,
        noun_data=noun
    )
    word = Word(
        surface_form="teach",
        entries=[entry1, entry2]
    )
    assert word.surface_form == "teach"
    assert len(word.entries) == 2
    assert isinstance(word.entries[0], LexicalEntry)
    assert isinstance(word.entries[1], LexicalEntry)
    assert word.entries[0].lemma == "teach"
    assert word.entries[1].lemma == "madra"

def test_word_rejects_invalid_entries():
    with pytest.raises(TypeError):
        Word(
            surface_form="teach",
            entries=["not a lexical entry"]
        )
