import pytest
from config import config
from db.mysql_db import MysqlRepository
from models.models import (
    Case,
    Declension,
    Gender,
    Mutation,
    Number,
    PartOfSpeech,
)

@pytest.fixture
def repository():
    """
    Create a repository for each test and close it afterward.
    """
    repo = MysqlRepository(config)
    yield repo
    repo.close()

def test_load_lexicon(repository):
    entries = repository.load_lexicon()
    assert len(entries) > 0
    lemmas = [entry.lemma for entry in entries]
    assert "teach" in lemmas
    assert "madra" in lemmas

def test_get_lexical_entry(repository):
    entry = repository.get_lexical_entry("teach")
    assert entry is not None
    assert entry.lemma == "teach"
    assert entry.definition == "house"
    assert entry.part_of_speech is PartOfSpeech.NOUN
    assert entry.noun_data is not None
    noun = entry.noun_data
    assert noun.gender is Gender.MASCULINE
    assert noun.declension is Declension.SECOND
    assert len(noun.forms) == 8
    assert any(
        form.surface_form == "teach"
        and form.case is Case.NOMINATIVE
        and form.number is Number.SINGULAR
        and form.mutation is Mutation.NONE
        for form in noun.forms
    )
    assert any(
        form.surface_form == "a theach"
        and form.case is Case.VOCATIVE
        and form.number is Number.SINGULAR
        and form.mutation is Mutation.LENITION
        for form in noun.forms
    )
    assert any(
        form.surface_form == "tí"
        and form.case is Case.GENITIVE
        and form.number is Number.SINGULAR
        for form in noun.forms
    )

def test_get_missing_lexical_entry(repository):
    entry = repository.get_lexical_entry(
        "word-that-is-not-in-the-database"
    )
    assert entry is None
