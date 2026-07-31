# Contains domain models and enumerations for the Irish Noun Morphological Parser
from enum import Enum

# Enumerations
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

# NounForm Class: Represents one inflected form of a noun.
class NounForm:
    def __init__(
        self,
        surface_form: str,
        case: Case,
        number: Number,
        mutation: Mutation
    ):
        if not isinstance(surface_form, str):
            raise TypeError("surface_form must be a string")
        if not isinstance(case, Case):
            raise TypeError("case must be a Case value")
        if not isinstance(number, Number):
            raise TypeError("number must be a Number value")
        if not isinstance(mutation, Mutation):
            raise TypeError("mutation must be a Mutation value")
        self.surface_form = surface_form
        self.case = case
        self.number = number
        self.mutation = mutation

# Noun Class: Stores noun-specific grammatical properties.
class Noun:
    def __init__(
        self,
        gender: Gender,
        declension: Declension,
        forms: list[NounForm]
    ):
        if not isinstance(gender, Gender):
            raise TypeError("gender must be a Gender value")
        if not isinstance(declension, Declension):
            raise TypeError("declension must be a Declension value")
        if not isinstance(forms, list):
            raise TypeError("forms must be a list of NounForm objects")
        if not all(isinstance(form, NounForm) for form in forms):
            raise TypeError("forms must contain only NounForm objects")
        self.gender = gender
        self.declension = declension
        self.forms = forms

# LexicalEntry Class: Represents one dictionary (lexical) entry.
class LexicalEntry:
    def __init__(
        self,
        lemma: str,
        definition: str,
        part_of_speech: PartOfSpeech,
        noun_data: Noun = None
    ):
        if not isinstance(lemma, str):
            raise TypeError("lemma must be a string")
        if not isinstance(definition, str):
            raise TypeError("definition must be a string")
        if not isinstance(part_of_speech, PartOfSpeech):
            raise TypeError("part_of_speech must be a PartOfSpeech value")
        if noun_data is not None and not isinstance(noun_data, Noun):
            raise TypeError("noun_data must be a Noun object")
        self.lemma = lemma
        self.definition = definition
        self.part_of_speech = part_of_speech
        self.noun_data = noun_data

# Word Class: Represents a surface form entered by the user.
class Word:
    def __init__(
        self,
        surface_form: str,
        entries: list[LexicalEntry]
    ):
        if not isinstance(surface_form, str):
            raise TypeError("surface_form must be a string")
        if not isinstance(entries, list):
            raise TypeError("entries must be a list of LexicalEntry objects")
        if not all(isinstance(entry, LexicalEntry) for entry in entries):
            raise TypeError("entries must contain only LexicalEntry objects")
        self.surface_form = surface_form
        self.entries = entries
