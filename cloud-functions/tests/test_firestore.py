import os
from google.cloud import firestore

# 서비스 계정 키 파일의 경로를 설정합니다.
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "../secrets/firebase-svc-account-key.json"


def test_firestore_connection():
    try:
        # Firestore 클라이언트를 초기화합니다.
        db = firestore.Client()

        # 테스트용 컬렉션 및 문서를 참조합니다.
        test_collection = db.collection("test_connection")
        test_doc = test_collection.document("test_doc")

        # 테스트용 데이터를 Firestore에 씁니다.
        test_data = {
            "message": "Firestore connection successful!",
            "timestamp": firestore.SERVER_TIMESTAMP,
        }
        test_doc.set(test_data)

        # Firestore에서 데이터를 읽습니다.
        read_data = test_doc.get().to_dict()
        print("Read data from Firestore:", read_data)

        return True

    except Exception as e:
        print("Firestore connection failed:", e)
        return False


if __name__ == "__main__":
    if test_firestore_connection():
        print("Firestore connection test passed.")
    else:
        print("Firestore connection test failed.")
