import abc
from typing import List
from models.models import LexicalEntry
class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_lexicon(self) -> List[LexicalEntry]:
        raise NotImplementedError
