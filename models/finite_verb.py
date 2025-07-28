from models.enums import Person, Number, Tense, Voice, Mood
class FiniteVerb:
    def __init__(self, person, number, tense, voice, mood):
        self.person = person
        self.number = number
        self.tense = tense
        self.voice = voice
        self.mood = mood
