import time
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from datetime import datetime

cred = credentials.Certificate("mobile-billing-chat-firebase-adminsdk-fbsvc-018cc52520.json") 
firebase_admin.initialize_app(cred)
db = firestore.client()

# Daha önce işlenen mesajları takip et
processed_ids = set()

while True:
    print("⏳ Firestore dinleniyor...")

    docs = db.collection("messages").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()

    for doc in docs:
        data = doc.to_dict()
        doc_id = doc.id

        if doc_id in processed_ids:
            continue

        if data.get("sender") == "user" and "response" not in data:
            print(f"🟢 Yeni mesaj bulundu: {data['text']}")

            try:
                res = requests.post(
                    "https://mobile-provider-api-vfpp.onrender.com/api/v1/gateway/chat",
                    json={"message": data["text"]},
                    timeout=15
                )
                res.raise_for_status()
                answer = res.json()
            except Exception as e:
                answer = {"error": str(e)}

            # Firestore'a yanıtı yaz
            db.collection("messages").document(doc_id).update({
                "response": answer,
                "processed_at": datetime.utcnow()
            })

            print(f"📬 Cevap yazıldı: {answer}")
            processed_ids.add(doc_id)

    time.sleep(5)
