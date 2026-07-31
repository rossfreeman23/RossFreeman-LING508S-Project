from typing import Optional
from config import config
from db.db_interface import Repository
from db.mysql_db import MysqlRepository
from models.models import PartOfSpeech
def generate_all_noun_forms_from_db(
    word: str,
    repository: Optional[Repository] = None
) -> dict:
    """
    Retrieve a noun and its complete morphological paradigm.
    A repository can be supplied during testing. If none is supplied,
    the service creates a MySQL repository.
    """
    if not isinstance(word, str):
        raise TypeError("word must be a string")
    normalized_word = word.strip()
    if not normalized_word:
        raise ValueError("word cannot be empty")
    owns_repository = repository is None
    if repository is None:
        repository = MysqlRepository(config)
    try:
        entry = repository.get_lexical_entry(normalized_word)
    finally:
        if owns_repository:
            repository.close()
    if (
        entry is None
        or entry.part_of_speech is not PartOfSpeech.NOUN
        or entry.noun_data is None
    ):
        raise ValueError(
            f"Noun '{normalized_word}' not found in database."
        )
    noun = entry.noun_data
    return {
        "lemma": entry.lemma,
        "definition": entry.definition,
        "part_of_speech": entry.part_of_speech.name.lower(),
        "gender": noun.gender.name.lower(),
        "declension": noun.declension.name.lower(),
        "forms": [
            {
                "surface_form": form.surface_form,
                "case": form.case.name.lower(),
                "number": form.number.name.lower(),
                "mutation": form.mutation.name.lower()
            }
            for form in noun.forms
        ]
    }
