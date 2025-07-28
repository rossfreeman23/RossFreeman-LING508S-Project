import pytest
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
