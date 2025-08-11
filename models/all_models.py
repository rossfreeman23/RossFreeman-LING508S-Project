#Model_Enumerations
from enum import Enum
class Gender(Enum):
    MASCULINE = 1
    FEMININE = 2
class Case(Enum):
    NOMINATIVE = 1
    GENITIVE = 2
    DATIVE = 3
    VOCATIVE = 4
class Number(Enum):
    SINGULAR = 1
    PLURAL = 2
class Declension(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
#Model_Noun_Form
from models.enums import Case, Number
class NounForm:
    def __init__(self, surface_form: str, case: Case, number: Number):
        self.surface_form = surface_form
        self.case = case
        self.number = number
#Model_Lexical_Entry
from models.noun import Noun
class LexicalEntry:
    def __init__(self, lemma: str, definition: str, part_of_speech: str, noun_data: Noun = None):
        self.lemma = lemma
        self.definition = definition
#Model_Noun
from models.enums import Gender, Declension
from models.noun_form import NounForm
class Noun:
    def __init__(self, gender: Gender, declension: Declension, forms: list[NounForm]):
        self.gender = gender
        self.declension = declension
        self.forms = forms
#Models_Word
from models.lexical_entry import LexicalEntry
class Word:
    def __init__(self, surface_form: str, entries: list[LexicalEntry]):
        self.surface_form = surface_form
        self.entries = entries
