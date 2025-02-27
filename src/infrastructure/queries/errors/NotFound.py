class NotFound(Exception):
    def __init__(self, entity_name: str, id: str):
        self.message = f'{entity_name} with id {id} does not exists'
        super().__init__(self.message)
