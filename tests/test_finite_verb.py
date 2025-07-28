import pytest
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
