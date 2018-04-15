class Sf:
    def __init__(self, session):
        self.client = session.client('stepfunctions')
