

class Cognito:
    def __init__(self, session):
        self.client = session.client("cognito-idp")
