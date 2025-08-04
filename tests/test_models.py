import pytest
#Finite_verb
from models.finite_verb import FiniteVerb
from models.enums import Person, Number, Tense, Mood, Voice
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
#Lexical_Entry
from models.lexical_entry import LexicalEntry
from models.enums import PartOfSpeech, Mutation
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
#Noun
from models.noun import Noun
from models.enums import Case, Number, Gender, Mutation
def test_noun_properties():
    noun = Noun(
        case=Case.GENITIVE,
        number=Number.SINGULAR,
        gender=Gender.MASCULINE,
        mutation=Mutation.LENITION
    )
    assert noun.case == Case.GENITIVE
    assert noun.mutation == Mutation.LENITION
