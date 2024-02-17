# Write me a fast api endpoint that takes a string or image as input and returns the same string or image

from fastapi import FastAPI, File, UploadFile, Body, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
# import hugging face auto model loader
from transformers import AutoModelForCausalLM, AutoTokenizer


app = FastAPI()

def get_image(image: UploadFile):
    img = Image.open(io.BytesIO(image.file.read()))
    return StreamingResponse(io.BytesIO(image.file.read()), media_type="image/png")

@app.post("/api/v0/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    print(f"Await start {file.__dict__}")
    content = await file.read()
    model = AutoModelForCausalLM.from_pretrained("hf-internal-testing/tiny-random-FuyuForCausalLM")
    tokenizer = AutoTokenizer.from_pretrained("hf-internal-testing/tiny-random-FuyuForCausalLM")
    '''inputs = tokenizer.encode("The capital of France is", return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, num_return_sequences=5)
    print(outputs)'''
    ## TODO: 
    model.forward()
    return Response(content=content, media_type="image/png")
    

@app.post("/api/v0/uploadstring")
async def create_upload_string(body: dict = Body(...)):
    print("Test recd")
    return body["string"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

