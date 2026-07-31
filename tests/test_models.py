#below needed to perform test
import pytest

#below needed to test models/classes/datatypes/enumerations
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

#Enumeration_Tests
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

#tests from here on out are sepcific to words to be used in the demo
#NounForm_Tests
def test_teach_noun_form_creation():
    form = NounForm(
        surface_form="teach",
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    assert form.surface_form == "teach"
    assert form.case == Case.NOMINATIVE
    assert form.number == Number.SINGULAR
    assert form.mutation == Mutation.NONE

def test_madra_mutated_form():
    form = NounForm(
        surface_form="mhadra",
        case=Case.VOCATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.LENITION
    )
    assert form.surface_form == "mhadra"
    assert form.case == Case.VOCATIVE
    assert form.number == Number.SINGULAR
    assert form.mutation == Mutation.LENITION

#Noun_Tests
def test_teach_noun_with_forms():
    nominative = NounForm(
        surface_form="teach",
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    genitive = NounForm(
        surface_form="tí",
        case=Case.GENITIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.FIRST,
        forms=[nominative, genitive]
    )
    assert noun.gender == Gender.MASCULINE
    assert noun.declension == Declension.FIRST
    assert len(noun.forms) == 2
    assert noun.forms[0].surface_form == "teach"
    assert noun.forms[1].surface_form == "tí"

def test_madra_noun_with_mutation():
    nominative = NounForm(
        surface_form="madra",
        case=Case.NOMINATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.NONE
    )
    vocative = NounForm(
        surface_form="mhadra",
        case=Case.VOCATIVE,
        number=Number.SINGULAR,
        mutation=Mutation.LENITION
    )
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.FIRST,
        forms=[nominative, vocative]
    )
    assert noun.gender == Gender.MASCULINE
    assert noun.forms[0].surface_form == "madra"
    assert noun.forms[1].surface_form == "mhadra"
    assert noun.forms[1].mutation == Mutation.LENITION

#LexicalEntry_Tests
def test_teach_lexical_entry():
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

def test_madra_lexical_entry():
    noun = Noun(
        gender=Gender.MASCULINE,
        declension=Declension.FIRST,
        forms=[]
    )
    entry = LexicalEntry(
        lemma="madra",
        definition="dog",
        part_of_speech=PartOfSpeech.NOUN,
        noun_data=noun
    )
    assert entry.lemma == "madra"
    assert entry.definition == "dog"

#Word_Tests
def test_word_with_teach_entry():
    entry = LexicalEntry(
        lemma="teach",
        definition="house",
        part_of_speech=PartOfSpeech.NOUN
    )
    word = Word(
        surface_form="teach",
        entries=[entry]
    )
    assert word.surface_form == "teach"
    assert len(word.entries) == 1
    assert word.entries[0].lemma == "teach"

def test_word_with_madra_entry():
    entry = LexicalEntry(
        lemma="madra",
        definition="dog",
        part_of_speech=PartOfSpeech.NOUN
    )
    word = Word(
        surface_form="madra",
        entries=[entry]
    )
    assert word.surface_form == "madra"
    assert word.entries[0].definition == "dog"
