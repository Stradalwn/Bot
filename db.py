from pymongo import MongoClient


class Database:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]

    async def add_rating(self, rate, user_id):
        rating = {
            "rate": rate,
            "user_id": user_id,
        }
        self.db.ratings.insert_one(rating)

    async def add_user(self, user_id, user_name):
        user = {
            "user_id": user_id,
            "user_name": user_name,
        }
        existing_user = self.db.users.find_one({"user_id": user_id})
        if existing_user:
            return existing_user, False
        else:
            new_user = self.db.users.insert_one(user)
            return new_user.inserted_id, True

    async def add_file(self, file_id, name, size):
        file = {
            "file_id": file_id,
            "name": name,
            "size": size,
        }
        self.db.files.insert_one(file)

    async def add_caption(self, user_id, caption):
        captions = {
            "user_id": user_id,
            "caption": caption,
        }
        existing_caption = self.db.captions.find_one({"user_id": user_id})
        if existing_caption:
            self.db.captions.delete_many({"user_id": user_id})

        new_caption = self.db.captions.insert_one(captions)
        return new_caption.inserted_id

    async def add_thumbnail(self, user_id, thumbnail):
        thumbnail = {
            "user_id": user_id,
            "thumbnail": thumbnail,
        }
        existing_thumb = self.db.thumbnails.find_one({"user_id": user_id})
        if existing_thumb:
            self.db.thumbnails.delete_many({"user_id": user_id})

        new_thumbnail = self.db.thumbnails.insert_one(thumbnail)
        return new_thumbnail.inserted_id

    async def get_user(self, user_id):
        return self.db.users.find_one({"user_id": user_id})

    async def get_all_user(self):
        return self.db.users.find()

    async def get_rating(self, user_id):
        return self.db.ratings.find_one({"user_id": user_id})

    async def get_file(self, file_id):
        return self.db.files.find_one({"file_id": file_id})

    async def get_caption(self, user_id):
        return self.db.captions.find_one({"user_id": user_id})

    async def get_thumbnail(self, user_id):
        return self.db.thumbnails.find_one({"user_id": user_id})

    async def delete_user(self, user_id):
        return self.db.users.delete_one({"user_id": user_id})

    async def delete_rating(self, user_id):
        self.db.ratings.delete_one({"user_id": user_id})

    async def delete_file(self, file_id):
        self.db.files.delete_one({"file_id": file_id})

    async def delete_caption(self, user_id):
        return self.db.captions.delete_one({"user_id": user_id})

    async def delete_thumbnail(self, user_id):
        return self.db.thumbnails.delete_one({"user_id": user_id})
