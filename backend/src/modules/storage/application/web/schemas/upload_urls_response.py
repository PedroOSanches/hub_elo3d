from pydantic import BaseModel


class UploadUrlResponseSchema(BaseModel):
    object_key: str
    upload_url: str

