import mysql.connector
from models.lexical_entry import LexicalEntry
from models.enums import PartOfSpeech, Mutation
from repository.repository_interface import Repository
class MysqlRepository(Repository):
    def __init__(self, config):
        self.conn = mysql.connector.connect(**config)
    def load_lexicon(self) -> list[LexicalEntry]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT form, part_of_speech, definition, mutation FROM lexical_entries")
        results = cursor.fetchall()
        cursor.close()
        entries = []
        for row in results:
            form, pos, definition, mutation = row
            entry = LexicalEntry(
                form=form,
                part_of_speech=PartOfSpeech(pos),
                definition=definition,
                mutation=Mutation(mutation)
            )
            entries.append(entry)
        return entries
    def close(self):
        self.conn.close()
