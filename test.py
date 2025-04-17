from deepface import DeepFace
import pickle
import os

rfid_id  = "667EF604"
folderPath = f"identityimage/{rfid_id}/{rfid_id}.pkl"

with open(folderPath, "rb") as f:
    data = pickle.load(f)

print(len(data['data']))

# data = {
#     'name': 'ryan lukito',
#     'rfid': rfid_id,
#     'data': []
# }

# for item in os.listdir(folderPath):
#     full_file_path = os.path.join(folderPath, item)
#     try:
#         # Gunakan path, bukan array
#         result = DeepFace.represent(img_path=full_file_path, enforce_detection=False)
#         embedding = result[0]["embedding"]
#         data['data'].append(embedding)
#         print(f"{item} -> success")
#         # os.remove(full_file_path) # perintah kontol
#     except Exception as e:
#         print(f"{item} -> failed: {e}")

# # Simpan pickle
# with open(f"identityimage/{rfid_id}.pkl", "wb") as f:
#     pickle.dump(data, f)

# print("Embedding saved.")


