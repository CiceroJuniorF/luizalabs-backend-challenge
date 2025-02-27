import uuid


class UUIDIdGenerator:
    def generate(self):
        return str(uuid.uuid4())