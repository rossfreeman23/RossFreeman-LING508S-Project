# Contains domain models and enumerations for the Irish noun morphological parser

#Enumerations
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
class Mutation(Enum):
    NONE = 1
    LENITION = 2
    ECLIPSIS = 3
class PartOfSpeech(Enum):
    NOUN = 1
    VERB = 2
    ADJECTIVE = 3

#NounForm_Class
class NounForm:
    def __init__(
        self,
        surface_form: str,
        case: Case,
        number: Number,
        mutation: Mutation
    ):
        self.surface_form = surface_form
        self.case = case
        self.number = number
        self.mutation = mutation

#Noun_Class
class Noun:
    def __init__(
        self,
        gender: Gender,
        declension: Declension,
        forms: list[NounForm]
    ):
        self.gender = gender
        self.declension = declension
        self.forms = forms

#LexicalEntry_Class
class LexicalEntry:
    def __init__(
        self,
        lemma: str,
        definition: str,
        part_of_speech: PartOfSpeech,
        noun_data: Noun = None
    ):
        self.lemma = lemma
        self.definition = definition
        self.part_of_speech = part_of_speech
        self.noun_data = noun_data

#Word_Class
class Word:
    def __init__(
        self,
        surface_form: str,
        entries: list[LexicalEntry]
    ):
        self.surface_form = surface_form
        self.entries = entries
