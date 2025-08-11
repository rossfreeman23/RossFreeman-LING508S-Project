import mysql.connector
from models.models import LexicalEntry
from models.enums import PartOfSpeech, Mutation
from repository.db_interface import Repository
from typing import List
class MysqlRepository(Repository):
    def __init__(self, config):
        self.conn = mysql.connector.connect(**config)
    def load_lexicon(self) -> List[LexicalEntry]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT form, part_of_speech, definition, mutation FROM lexical_entries")
        results = cursor.fetchall()
        cursor.close()
        entries = []
        for row in results:
            form, pos, definition, mutation = row
            entry = LexicalEntry(
                lemma=form,
                part_of_speech=PartOfSpeech(pos.lower()),
                definition=definition,
                mutation=Mutation(mutation.lower())
            )
            entries.append(entry)
        return entries
    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()
