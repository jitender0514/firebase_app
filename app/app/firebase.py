import firebase_admin
import uuid
import os
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore

from django.utils import timezone
from django.conf import settings

FIREBASE_MODE="test"

TITLE_COLLECTION = f"{FIREBASE_MODE}_titles1"
OUTLINE_COLLECTION = f"{FIREBASE_MODE}_outlines1"
COLLECTION_NAMES = [TITLE_COLLECTION, OUTLINE_COLLECTION]

# Firebase Account Auth
FIREBASE_ACCOUNT_TYPE="service_account"
FIREBASE_PROJECT_ID="testing-7b5d5"
FIREBASE_PRIVATE_KEY_ID="42e7c3fbaaa87a57477416309bc3f77f30575a20"
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzR+uLx058vFk2\nywBiZDXFaZtqn3EdOkpQewwuq5ed9Je6gR6L/FxymV9+KKa1CAnb+f0404EOS/nA\nK433J14B6+KcEBrwWMvYEeU2ZON7nWe4OnnbvhqsjNPwsDqCz64hdii/JaGQQfx/\njVms3ymwC5VESix7TtSHlORgrB/gqEjzmeQ9v8RyuObMUAzYwM8Ahwhw4fvyta7b\nMQSjGCBKTKhtLuQHBdcfPR7kuI/wd03oyvAmrWtsp1SL5/2UB7WOwz22vFeRjw3D\n5mAijGj/S1m4TcLix1Vx+lOwfxN4n06qVw3bqMC0TahMU4KlKh1aTa02GCZDa9Xe\nMMD+2HFlAgMBAAECggEAG6WjJt6Y9XZsQZ1jlUjD3Aoxq+sjm/DBxhB7q/TNQFAY\nV+wShF7p+Mg7KC7nqnIvZwtxp+JB/CzuOlrdHTimcCBqxUtchCUFZnA4Cz/artTy\nyj/GTANQhLyA8JSUqViSj1lz5ipM9HygjiEDq7uMZ7gZkDrqCif5cWEeKORSVCgN\nIHCH4khx0+EXtWkdu4TuiqiSWAb7OXNtcxoVYxSuZGnyMU8e741q4z4K2vtdJ49W\nKa1WjSUGdWw3HCYLldJL1WJZ5mAQ+eiPDbGqUereOOu4krqtbcIiw2yAuyvN73m5\nDZXpVhoFUt6tTk8BDL3UIyR/QITZ9StvDD1KucLO7wKBgQDq+lmU4yk8DuIvyMP/\nYw4GsWQCE4MAvX9k9V9DCkvdrAb/qN1qoCpXi7fAx4552VEK/N8PpOpA/47JxOHo\n+ozNXvg701g9Vu3nsL84ZhgX8/XZcKvEMh/rEJYlmE5VUQqT6iy75eqdfOyDdfzz\noZsleZi+SrnurYnArNIVhg6HAwKBgQDDUfQlfNn8AGtp7xJwQcRpJ2DOJEs0ZH/w\nV4nhyZUKfyhzZvsnvtIDgTV/uf2xDNCgfbjhpa2/E/RRrIMA1SlARJwZ68A4OHz6\nZirQqVAHCODeQZkMn5Es0FS8wztdul2cNQ11VVE7bBD7Xz18POv/IrbFu2cSFWK3\nhGtFwcbldwKBgDfuv8QhDn+tS0n0kDMKcRxGvXeBDX3vnZN6lOJwYP6zJDdXCt2G\noo2URHkvB0sZ36Ct8KrYpqoyKtr8conymfGI2a3j8O0o9BhiiiHyq2mIOM05dKmP\nBOn/WL46Mus8DziGVX+kiuRSCDqCq2OS5EtXVnR1dSzLQi8K9DcLYgnhAoGAQgmd\ncGdMFEXYC1MHeujhjWQA+PGQc8Be+VW/ipVrTMc9V/dDh2ae/wxamDq8KXZZu0mG\njtRDcE1A17Rp/ogTkGUiGil5Lgj7SHXul+oG4rn/vWWUZ44zuWEepUuk8MWoDL5r\nNHaKJnsdKsBCu5SlffewsB3ydUzBuaaN1mHz63UCgYEA0j07kD6gTb/6V4wITpQh\nrTMS+MwL2iH5t1jxZXfRgWESpfisJPu9pWvvpKcSrTCh+Yh/A9i4JISw9XA06PMB\n4brJ1F23s/0F97Ue6gAidNtTmBYxfQugkemX5KX4US14EgVzZaSB8ldm8nERT942\nB+T0fUhbC+xv2eBX3XrElBE=\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL="firebase-adminsdk-50eim@testing-7b5d5.iam.gserviceaccount.com"
FIREBASE_CLIENT_ID="111826599702814973420"
FIREBASE_AUTH_URI="https://accounts.google.com/o/oauth2/auth"
FIREBASE_TOKEN_URI="https://oauth2.googleapis.com/token"
FIREBASE_AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
FIREBASE_CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-50eim%40testing-7b5d5.iam.gserviceaccount.com"


try:
    CRED = credentials.Certificate({
        "type": FIREBASE_ACCOUNT_TYPE,
        "project_id": FIREBASE_PROJECT_ID,
        "private_key_id": FIREBASE_PRIVATE_KEY_ID,
        "private_key": FIREBASE_PRIVATE_KEY,
        "client_email": FIREBASE_CLIENT_EMAIL,
        "client_id": FIREBASE_CLIENT_ID,
        "auth_uri": FIREBASE_AUTH_URI,
        "token_uri": FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": FIREBASE_CLIENT_X509_CERT_URL,
    })
    FB_APP = initialize_app(CRED)
except ValueError as e:
    print(e)
    raise BrokenPipeError("Firebase not configured properly. Please check the environment variaables!!")
    CRED = None
    FB_APP = None


class Firebase:
    cert_file = None
    app = None
    db = None
    output_fields = ["created_at", "generation_id", "like_status", "output"]

    COLLECTION = TITLE_COLLECTION
    FIELDS = [
        "text",
        "name",
        "generation_id",
        "updated_at",
        "created_at",
        "old_record",
        "is_deleted"
    ]

    def set_collection(self, collection):
        if collection in COLLECTION_NAMES:
            self.COLLECTION = collection

    def __init__(self, cert_path="bramework-app-dev-firebase-adminsdk-54vkw-0969002993.json") -> None:
        # self.cert_file = cert_path
        # cred = credentials.Certificate(self.cert_file)
        self.app = FB_APP
        self.db = firestore.client()

    def set_field_data(self, obj):
        DATA = {}
        for field in self.FIELDS:
            DATA[field] = obj[field] if field in obj and obj[field] else None
            if field in ["updated_at", "created_at"] and not DATA[field]:
                DATA[field] = timezone.now()
            if field == "generation_id":
                DATA[field] = str(uuid.uuid4())

            if field == "old_record":
                if "old_record" in obj:
                    DATA[field] = obj[field]
                else:
                    DATA[field] = False
            if field == "is_deleted":
                if "is_deleted" in obj:
                    DATA[field] = obj[field]
                else:
                    DATA[field] = False
        return DATA

    def batch_save_data(self, data_list):
        new_list = []
        for obj in data_list:
            new_list.append(self.set_field_data(obj))

        batch = self.db.batch()
        for new_obj in new_list:
            doc_ref = self.db.collection(self.COLLECTION).document(new_obj["generation_id"])
            doc_ref.set(new_obj)
        # Commit the batch
        batch.commit()

    def save_data(self, fetch_record=True, **data):
        DATA = {}
        for field in self.FIELDS:
            DATA[field] = data[field] if field in data and data[field] else None
            if field in ["updated_at", "created_at"] and not DATA[field]:
                DATA[field] = timezone.now()
            if field == "generation_id":
                DATA[field] = str(uuid.uuid4())

            if field == "old_record":
                if "old_record" in data:
                    DATA[field] = data[field]
                else:
                    DATA[field] = False
            if field == "is_deleted":
                if "is_deleted" in data:
                    DATA[field] = data[field]
                else:
                    DATA[field] = False

        doc_ref = self.db.collection(
            self.COLLECTION).document(DATA["generation_id"])
        doc_ref.set(DATA)
        if fetch_record:
            snapshot = doc_ref.get()
            obj_dict = snapshot.to_dict()
            return {field: obj_dict[field] for field in self.output_fields if field in obj_dict}
        else:
            return DATA

    def update_data(self, ref_id, update_data, fetch_record=True, ):
        DATA = {}
        for field in update_data:
            if field in self.FIELDS:
                DATA[field] = update_data[field]
        DATA["updated_at"] = timezone.now()
        doc_ref = self.db.collection(self.COLLECTION).document(ref_id)

        doc_ref.update(DATA)
        snapshot = doc_ref.get()
        return snapshot.to_dict()

    def update_post(self, ref_id, post_id):
        data = {"post_id": post_id}
        return self.update_data(ref_id, data)

    def soft_delete(self, ref_id):
        return self.update_data(ref_id, {"is_deleted": True})

    def update_like_status(self, ref_id, user_id, like_dislike_flag):
        doc_ref = self.db.collection(self.COLLECTION).document(ref_id)
        snapshot = doc_ref.get()
        record = snapshot.to_dict()

        if "like_status" in record and record["like_status"]:
            like_status = record["like_status"]
            found_index = None
            for index, user_status in enumerate(like_status):
                if "user_id" in user_status and user_status["user_id"] == user_id:
                    found_index = index
            if found_index == None:
                like_status.append(
                    {"user_id": user_id, "status": like_dislike_flag})
            else:
                like_status[found_index] = {
                    "user_id": user_id, "status": like_dislike_flag}
            return self.update_data(ref_id, {"like_status": like_status})
        return self.update_data(ref_id, {"like_status": [{"user_id": user_id, "status": like_dislike_flag}]})

    def delete_like_status(self, ref_id, user_id):
        doc_ref = self.db.collection(self.COLLECTION).document(ref_id)
        snapshot = doc_ref.get()
        record = snapshot.to_dict()

        if "like_status" in record and record["like_status"]:
            like_status = record["like_status"]
            new_like_status = []
            for index, user_status in enumerate(like_status):
                if "user_id" in user_status and user_status["user_id"] != user_id:
                    new_like_status.append(user_status)
            new_like_status = new_like_status if new_like_status else None
            return self.update_data(ref_id, {"like_status": new_like_status})
        return record

    def fetch_data(self, condition=None):
        # output_fields = [ "created_at", "generation_id", "like_status", "output"]
        doc_ref = self.db.collection(self.COLLECTION)

        if condition:
            doc_ref = doc_ref.where(condition['field'], condition['oprator'], condition['value']).where(
                "is_deleted", '==', False)
        else:
            doc_ref = doc_ref.where("is_deleted", '==', False)
        docs = doc_ref.stream()
        DATA = []
        for obj in docs:
            obj_dict = obj.to_dict()
            DATA.append({field: obj_dict[field] for field in self.output_fields if field in obj_dict})
        return DATA

    def check_generation_id_exists(self, generation_id):
        doc_ref = self.db.collection(self.COLLECTION).document(generation_id)
        snapshot = doc_ref.get()
        record = snapshot.to_dict()
        if record:
            return True
        return False
