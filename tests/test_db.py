import pytest
from repository.mysql_repository import MysqlRepository
from config import config
def test_load_lexicon():
    repo = MysqlRepository(config)
    entries = repo.load_lexicon()
    repo.close()
    assert len(entries) >= 2
    first = entries[0]
    assert first.form == "teach"
    assert first.definition == "house"
    assert first.part_of_speech == PartOfSpeech.NOUN
    assert first.mutation == Mutation.NONE
