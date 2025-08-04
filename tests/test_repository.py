import pytest
from repository.mysql_repository import MysqlRepository
from config import config
def test_load_lexicon():
    repo = MysqlRepository(config)
    entries = repo.load_lexicon()
    repo.close()
    assert len(entries) >= 2
    assert entries[0].form == "teach"
    assert entries[0].definition == "house"
