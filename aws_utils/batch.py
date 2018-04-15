class Batch:
    def __init__(self, session):
        self.client = session.client('batch')
