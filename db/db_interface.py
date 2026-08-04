# db/db_interface.py: Defines the abstract repository interface used by the service layer.
# The interface separates database operations from the application’s domain models and business logic.

import abc
from typing import List, Optional
from models.models import LexicalEntry

class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_lexicon(self) -> List[LexicalEntry]:
        raise NotImplementedError
    @abc.abstractmethod
    def get_lexical_entry(
        self,
        lemma: str
    ) -> Optional[LexicalEntry]:
        raise NotImplementedError
