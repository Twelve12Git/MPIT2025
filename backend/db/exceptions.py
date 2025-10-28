
class EntityAlreadyExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class EntityNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)