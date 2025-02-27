from bson import ObjectId


class MongoDBIdGenerator:
    def generate(self):
        return str(ObjectId())