import pytest
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
