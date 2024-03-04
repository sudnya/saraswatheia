from fastapi import FastAPI, File, UploadFile, Body, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
from transformers import FuyuForCausalLM, FuyuProcessor

TINY_FUYU = "hf-internal-testing/tiny-random-FuyuForCausalLM"
ADEPT_FUYU = "adept/fuyu-8b"

CURRENT_FUYU = TINY_FUYU
app = FastAPI()


IMAGE_IN_MEMORY = None

def get_image(image: UploadFile):
    img = Image.open(io.BytesIO(image.file.read()))
    return StreamingResponse(io.BytesIO(image.file.read()), media_type="image/png")

def model_stuff(prompt: str):
    return fuyu_stuff(prompt)

def fuyu_stuff(text_prompt: str = None):
    processor = FuyuProcessor.from_pretrained(CURRENT_FUYU)
    model = FuyuForCausalLM.from_pretrained(CURRENT_FUYU)
    print(f"\n\n\n image in memory type is {type(IMAGE_IN_MEMORY)}\n\n\n")

    byte_stream = io.BytesIO(IMAGE_IN_MEMORY)
    actual_bytes = byte_stream.getvalue()
    
    image = Image.open(byte_stream)
    print(f"\n\n image is of type {type(image)}\n\n")
    # Get the image data as a bytes object
    image_data = image.tobytes()

    # Convert the image data to a NumPy array
    arr = np.frombuffer(image_data, dtype=np.uint8)
    
    print("Size:", image.size)
    size_dict = {}
    size_dict["height"] = image.size[1]
    size_dict["width"]=  image.size[0]
    
    import traceback
    try:
        processor.image_processor.size = {"height": 300, "width": 300}
        print("Processor size", processor.__dict__)
        inputs = processor(text=text_prompt, images=[image], return_tensors="pt")
    except Exception as e:
        traceback.print_exc()

    generated_ids = model.generate(**inputs, max_new_tokens=7)
    generation_text = processor.batch_decode(generated_ids, skip_special_tokens=True)
    return generation_text


@app.post("/api/v0/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    print(f"Await start {file.__dict__}")
    content = await file.read()
    
    global IMAGE_IN_MEMORY
    IMAGE_IN_MEMORY = content

    return Response(content=content, media_type="image/png")
    

@app.post("/api/v0/uploadstring")
async def create_upload_string(body: dict = Body(...)):
    # curl -X POST -H "Content-Type: application/json" -d '{"string": "test this"}' http://127.0.0.1:8000/api/v0/uploadstring
    return model_stuff(body["string"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
