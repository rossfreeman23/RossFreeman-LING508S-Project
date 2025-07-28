from models.enums import PartOfSpeech, Mutation
class LexicalEntry:
    def __init__(self, form, part_of_speech, definition, mutation):
        self.form = form
        self.part_of_speech = part_of_speech
        self.definition = definition
        self.mutation = mutation
