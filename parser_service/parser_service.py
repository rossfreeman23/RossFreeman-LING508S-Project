from repository.mysql_repository import MysqlRepository
from config import config
def generate_all_noun_forms_from_db(word: str) -> dict:
    repo = MysqlRepository(config)
    entries = repo.load_lexicon()
    for entry in entries:
        if entry.lemma.lower() == word.lower() and entry.part_of_speech.name.lower() == "noun":
            noun = entry.noun_data
            if noun:
                return {
                    "lemma": entry.lemma,
                    "definition": entry.definition,
                    "gender": noun.gender.name.lower(),
                    "declension": noun.declension.name.lower(),
                    "forms": [
                        {
                            "surface_form": form.surface_form,
                            "case": form.case.name.lower(),
                            "number": form.number.name.lower()
                        } for form in noun.forms
                    ]
                }
    raise ValueError(f"Noun '{word}' not found in database.")
