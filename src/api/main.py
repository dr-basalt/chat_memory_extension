
from fastapi import FastAPI, UploadFile, File
from src.utils.ocr import process_image
from src.utils.minio import upload_to_minio
from src.utils.encryption import encrypt_data
import redis, os, json

app = FastAPI()
r = redis.Redis(host='redis', port=int(os.getenv('REDIS_PORT', 6379)), decode_responses=True)

@app.post("/memorize/image")
async def memorize_image(file: UploadFile = File(...)):
    content = await file.read()
    text = process_image(content)
    image_path = upload_to_minio(file.filename, content)
    payload = {
        "filename": file.filename,
        "ocr_text": text,
        "minio_path": image_path
    }
    r.set(f"image:{file.filename}", json.dumps(payload))
    return {"message": "Image processed and stored", "data": payload}
