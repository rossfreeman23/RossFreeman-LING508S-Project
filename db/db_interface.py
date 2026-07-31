import abc
from typing import List, Optional
from models.models import LexicalEntry

class Repository(metaclass=abc.ABCMeta):
    """
    Defines the database operations available to the service layer.
    Repository implementations are responsible for constructing complete
    LexicalEntry objects, including noun properties and noun forms.
    """
    @abc.abstractmethod
    def load_lexicon(self) -> List[LexicalEntry]:
        """
        Return all lexical entries in the repository.
        """
        raise NotImplementedError
    @abc.abstractmethod
    def get_lexical_entry(
        self,
        lemma: str
    ) -> Optional[LexicalEntry]:
        """
        Return the complete lexical entry for a lemma.
        Return None when the lemma is not found.
        """
        raise NotImplementedError
        
