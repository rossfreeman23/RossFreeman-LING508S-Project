#Model_Enumerations
from enum import Enum
class Gender(Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
class Tense(Enum):
    PRESENT = "present"
    PAST = "past"
    FUTURE = "future"
class Mood(Enum):
    INDICATIVE = "indicative"
    IMPERATIVE = "imperative"
    SUBJUNCTIVE = "subjunctive"
class Case(Enum):
    NOMINATIVE = "nominative"
    GENITIVE = "genitive"
    DATIVE = "dative"
    VOCATIVE = "vocative"
class Number(Enum):
    SINGULAR = "singular"
    PLURAL = "plural"
class Mutation(Enum):
    NONE = "none"
    LENITION = "lenition"
    ECLIPSIS = "eclipsis"
class Voice(Enum):
    ACTIVE = "active"
    PASSIVE = "passive"
class Person(Enum):
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"
class PartOfSpeech(Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    PREPOSITION = "preposition"
#Model_Finite_Verb
from models.enums import Person, Number, Tense, Voice, Mood
class FiniteVerb:
    def __init__(self, person, number, tense, voice, mood):
        self.person = person
        self.number = number
        self.tense = tense
        self.voice = voice
        self.mood = mood
#Model_Lexical_Entry
from models.enums import PartOfSpeech, Mutation
class LexicalEntry:
    def __init__(self, form, part_of_speech, definition, mutation):
        self.form = form
        self.part_of_speech = part_of_speech
        self.definition = definition
        self.mutation = mutation
#Model_Noun
from models.enums import Case, Number, Gender, Mutation
class Noun:
    def __init__(self, case, number, gender, mutation):
        self.case = case
        self.number = number
        self.gender = gender
        self.mutation = mutation
#Models_Word
class Word:
    def __init__(self, lexical_entry, surface_form):
        self.lexical_entry = lexical_entry
        self.surface_form = surface_form
