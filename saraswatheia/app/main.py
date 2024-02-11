# Write me a fast api endpoint that takes a string or image as input and returns the same string or image

from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI()

def get_image(image: UploadFile):
    img = Image.open(io.BytesIO(image.file.read()))
    return StreamingResponse(io.BytesIO(image.file.read()), media_type="image/png")

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    return get_image(file)

@app.post("/uploadstring")
async def create_upload_string(body: dict = Body(...)):
    return body["string"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

