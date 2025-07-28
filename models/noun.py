from models.enums import Case, Number, Gender, Mutation
class Noun:
    def __init__(self, case, number, gender, mutation):
        self.case = case
        self.number = number
        self.gender = gender
        self.mutation = mutation
