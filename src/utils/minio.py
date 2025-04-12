
from minio import Minio
import os

client = Minio(
    "minio:9000",
    access_key="minio",
    secret_key="miniopass",
    secure=False
)

def upload_to_minio(filename, data):
    bucket = "memoires"
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    with open(f"/tmp/{filename}", "wb") as f:
        f.write(data)
    client.fput_object(bucket, filename, f"/tmp/{filename}")
    return f"s3://{bucket}/{filename}"
