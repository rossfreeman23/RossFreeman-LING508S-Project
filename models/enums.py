
#Enumerations
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
