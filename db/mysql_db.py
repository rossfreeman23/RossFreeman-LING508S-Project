# db/mysql_db.py: Implements the repository interface for a MySQL database.
# It retrieves lexical entries, noun properties, and noun forms from the normalized
# database tables and converts the returned rows into domain model objects.

from typing import Dict, List, Optional
import mysql.connector
from db.db_interface import Repository
from models.models import (
    Case,
    Declension,
    Gender,
    LexicalEntry,
    Mutation,
    Noun,
    NounForm,
    Number,
    PartOfSpeech,
)

class MysqlRepository(Repository):
    def __init__(self, config: dict):
        self.conn = mysql.connector.connect(**config)
    def load_lexicon(self) -> List[LexicalEntry]:
        return self._fetch_entries()
    def get_lexical_entry(
        self,
        lemma: str
    ) -> Optional[LexicalEntry]:
        entries = self._fetch_entries(lemma)
        if not entries:
            return None
        return entries[0]
    def _fetch_entries(
        self,
        lemma: Optional[str] = None
    ) -> List[LexicalEntry]:
        query = """
            SELECT
                le.id AS lexical_entry_id,
                le.lemma,
                le.part_of_speech,
                le.definition,
                n.id AS noun_id,
                n.gender,
                n.declension,
                nf.id AS noun_form_id,
                nf.surface_form,
                nf.grammatical_case,
                nf.grammatical_number,
                nf.mutation
            FROM lexical_entries AS le
            LEFT JOIN nouns AS n
                ON n.lexical_entry_id = le.id
            LEFT JOIN noun_forms AS nf
                ON nf.noun_id = n.id
        """
        parameters = ()
        if lemma is not None:
            query += """
                WHERE le.lemma = %s
            """
            parameters = (lemma,)
        query += """
            ORDER BY le.id, nf.id
        """
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(query, parameters)
            rows = cursor.fetchall()
        finally:
            cursor.close()
        return self._build_entries(rows)

    def _build_entries(
        self,
        rows: List[dict]
    ) -> List[LexicalEntry]:
        entries: Dict[int, LexicalEntry] = {}
        for row in rows:
            lexical_entry_id = row["lexical_entry_id"]
            if lexical_entry_id not in entries:
                noun_data = None
                if row["noun_id"] is not None:
                    noun_data = Noun(
                        gender=Gender(row["gender"]),
                        declension=Declension(
                            row["declension"]
                        ),
                        forms=[]
                    )
                entries[lexical_entry_id] = LexicalEntry(
                    lemma=row["lemma"],
                    definition=row["definition"],
                    part_of_speech=PartOfSpeech(
                        row["part_of_speech"]
                    ),
                    noun_data=noun_data
                )
            entry = entries[lexical_entry_id]
            if (
                entry.noun_data is not None
                and row["noun_form_id"] is not None
            ):
                noun_form = NounForm(
                    surface_form=row["surface_form"],
                    case=Case(
                        row["grammatical_case"]
                    ),
                    number=Number(
                        row["grammatical_number"]
                    ),
                    mutation=Mutation(
                        row["mutation"]
                    )
                )
                entry.noun_data.forms.append(noun_form)
        return list(entries.values())
    def close(self) -> None:
        if self.conn.is_connected():
            self.conn.close()
    def __del__(self):
        try:
            self.close()
        except (AttributeError, mysql.connector.Error):
            pass
