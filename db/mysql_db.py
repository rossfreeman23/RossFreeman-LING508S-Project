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
    """
    MySQL implementation of the Repository interface.
    """
    def __init__(self, config: dict):
        self.conn = mysql.connector.connect(**config)
    def load_lexicon(self) -> List[LexicalEntry]:
        """
        Return every lexical entry, including its noun data and forms.
        """
        return self._fetch_entries()
    def get_lexical_entry(
        self,
        lemma: str
    ) -> Optional[LexicalEntry]:
        """
        Return the complete lexical entry for a lemma.

        Return None when the lemma does not exist.
        """
        entries = self._fetch_entries(lemma)
        if not entries:
            return None
        return entries[0]
    def _fetch_entries(
        self,
        lemma: Optional[str] = None
    ) -> List[LexicalEntry]:
        """
        Retrieve database rows and convert them into domain objects.
        When lemma is supplied, only entries matching that lemma are
        retrieved. Otherwise, the complete lexicon is retrieved.
        """
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
        """
        Convert joined database rows into complete LexicalEntry objects.
        """
        entries: Dict[int, LexicalEntry] = {}
        for row in rows:
            lexical_entry_id = row["lexical_entry_id"]
            if lexical_entry_id not in entries:
                noun_data = None
                if row["noun_id"] is not None:
                    noun_data = Noun(
                        gender=Gender[row["gender"].upper()],
                        declension=Declension[
                            row["declension"].upper()
                        ],
                        forms=[]
                    )
                entries[lexical_entry_id] = LexicalEntry(
                    lemma=row["lemma"],
                    definition=row["definition"],
                    part_of_speech=PartOfSpeech[
                        row["part_of_speech"].upper()
                    ],
                    noun_data=noun_data
                )
            entry = entries[lexical_entry_id]
            if (
                entry.noun_data is not None
                and row["noun_form_id"] is not None
            ):
                noun_form = NounForm(
                    surface_form=row["surface_form"],
                    case=Case[
                        row["grammatical_case"].upper()
                    ],
                    number=Number[
                        row["grammatical_number"].upper()
                    ],
                    mutation=Mutation[
                        row["mutation"].upper()
                    ]
                )
                entry.noun_data.forms.append(noun_form)
        return list(entries.values())
    def close(self) -> None:
        """
        Close the MySQL connection.
        """
        if self.conn.is_connected():
            self.conn.close()
    def __del__(self):
        """
        Close the connection if the repository is destroyed.
        """
        try:
            self.close()
        except (AttributeError, mysql.connector.Error):
            pass
