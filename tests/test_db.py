import pytest
from repository.mysql_repository import MysqlRepository
from config import config
from models.enums import PartOfSpeech, Mutation
def test_load_lexicon():
    repo = MysqlRepository(config)
    entries = repo.load_lexicon()
    assert len(entries) > 0
    match = [e for e in entries if e.lemma == "teach" and e.definition == "house"]
    assert match, "Expected entry for 'teach' not found"
    entry = match[0]
    assert entry.part_of_speech == PartOfSpeech.NOUN
    assert entry.mutation == Mutation.NONE
