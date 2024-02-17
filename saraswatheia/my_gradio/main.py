import gradio as gr
import requests
from PIL import Image
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
from tempfile import NamedTemporaryFile
import shutil
import numpy as np

# FastAPI endpoint URL
FASTAPI_ENDPOINT_STRING = "http://localhost:8000/api/v0/uploadstring" 
FASTAPI_ENDPOINT_FILE = "http://localhost:8000/api/v0/uploadfile"

def pil_image_to_upload_file(pil_image: Image.Image) -> UploadFile:
    # Save the PIL image to a temporary file
    temp_file = NamedTemporaryFile(delete=False, suffix=".jpg")
    pil_image.save(temp_file.name)
    # Create an UploadFile object from the temporary file
    file = {'file': open(temp_file.name, 'rb')}
    return  file

def fastapi_predict_text(text):
    # Sending a POST request to the FastAPI endpoint
    response = requests.post(FASTAPI_ENDPOINT_STRING, json={"string": text})
    # Assuming the FastAPI endpoint returns a JSON response
    result = response.json()

    return result

def fastapi_predict_image(image_arr):
    image = Image.fromarray(image_arr)
    # Sending a POST request to the FastAPI endpoint
    temp = pil_image_to_upload_file(image)
    response = requests.post(FASTAPI_ENDPOINT_FILE, files=temp)#("file", temp)])
    # Convert the response content to a PIL image
    # Convert the image content to a NumPy array
    print(f"Content type {response.__dict__}")
    image_content = BytesIO(response.content)

    # print the first 10 bytes of the file
    # then reset the file pointer to the start
    print(f"First 10 bytes: {image_content.read(10)}")
    image_content.seek(0)

    image = Image.open(image_content)
    image_array = np.array(image)
    
    return image_array


with gr.Blocks() as demo:

    # Gradio interface with two components
    text_component = gr.Interface(
        fn=fastapi_predict_text,
        inputs=gr.Textbox(),
        outputs="text",
        live=True
    )

    image_component = gr.Interface(
        fn=fastapi_predict_image,
        inputs=gr.Image(),
        outputs="image",
        live=True
    )


# Launch the Gradio interfaces
demo.launch(share=True)


