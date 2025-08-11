import pytest
from models.models import (
    Word, LexicalEntry, Noun, NounForm,
    Gender, Declension, Case, Number
)
#test_enum
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
#test_nounform
def test_noun_form_creation():
    nf = NounForm(surface_form="bháid", case=Case.GENITIVE, number=Number.PLURAL)
    assert nf.surface_form == "bháid"
    assert nf.case == Case.GENITIVE
    assert nf.number == Number.PLURAL
def test_noun_with_forms():
    form1 = NounForm("bád", Case.NOMINATIVE, Number.SINGULAR)
    form2 = NounForm("báid", Case.NOMINATIVE, Number.PLURAL)
    noun = Noun(gender=Gender.MASCULINE, declension=Declension.FIRST, forms=[form1, form2])
    assert noun.gender == Gender.MASCULINE
    assert noun.declension == Declension.FIRST
    assert len(noun.forms) == 2
    assert noun.forms[0].surface_form == "bád"
#test_lexicalentry
def test_lexical_entry_basic():
    entry = LexicalEntry(lemma="bád", definition="boat")
    assert entry.lemma == "bád"
    assert entry.definition == "boat"
#test_word
def test_word_with_entries():
    entry1 = LexicalEntry("bád", "boat")
    entry2 = LexicalEntry("báid", "boats")
    word = Word(surface_form="báid", entries=[entry1, entry2])
    assert word.surface_form == "báid"
    assert len(word.entries) == 2
    assert word.entries[0].definition == "boat"
