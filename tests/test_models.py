import pytest
from models.enums import (
    Gender, Tense, Mood, Case, Number, Mutation, Voice, Person, PartOfSpeech
)
from models.finite_verb import FiniteVerb
from models.lexical_entry import LexicalEntry
from models.noun import Noun
from models.word import Word
#enum_tests
def test_enum_gender():
    assert Gender.MASCULINE.value == "masculine"
    assert Gender.FEMININE.value == "feminine"
def test_enum_tense():
    assert Tense.PRESENT.value == "present"
    assert Tense.PAST.value == "past"
    assert Tense.FUTURE.value == "future"
def test_enum_mood():
    assert Mood.IMPERATIVE.value == "imperative"
def test_enum_case():
    assert Case.DATIVE.value == "dative"
def test_enum_number():
    assert Number.PLURAL.value == "plural"
def test_enum_mutation():
    assert Mutation.ECLIPSIS.value == "eclipsis"
def test_enum_voice():
    assert Voice.PASSIVE.value == "passive"
def test_enum_person():
    assert Person.SECOND.value == "second"
def test_enum_part_of_speech():
    assert PartOfSpeech.ADJECTIVE.value == "adjective"
#finite_verb_tests
def test_finite_verb_creation():
    verb = FiniteVerb(
        person=Person.FIRST,
        number=Number.SINGULAR,
        tense=Tense.PAST,
        voice=Voice.ACTIVE,
        mood=Mood.INDICATIVE
    )
    assert verb.tense == Tense.PAST
    assert verb.voice == Voice.ACTIVE
def test_lexical_entry_creation():
    entry = LexicalEntry(
        form="teach",
        part_of_speech=PartOfSpeech.NOUN,
        definition="house",
        mutation=Mutation.NONE
    )
    assert entry.form == "teach"
    assert entry.definition == "house"
    assert entry.mutation == Mutation.NONE
#noun_tests
def test_noun_properties():
    noun = Noun(
        case=Case.GENITIVE,
        number=Number.SINGULAR,
        gender=Gender.MASCULINE,
        mutation=Mutation.LENITION
    )
    assert noun.case == Case.GENITIVE
    assert noun.mutation == Mutation.LENITION
#word_tests
def test_word_creation():
    lex_entry = LexicalEntry(
        form="madra",
        part_of_speech=PartOfSpeech.NOUN,
        definition="dog",
        mutation=Mutation.NONE
    )
    word = Word(lexical_entry=lex_entry, surface_form="madra")
    assert word.lexical_entry.definition == "dog"
    assert word.surface_form == "madra"
