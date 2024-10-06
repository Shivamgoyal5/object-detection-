from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests
import io
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model and processor
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

@app.post("/detect/")
# async def detect_objects(file: UploadFile = File(...)):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))

#     # Process the image
#     inputs = processor(images=image, return_tensors="pt")
#     outputs = model(**inputs)

    # Convert outputs to COCO API format@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Convert the image to RGB if it's not already
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Process the image
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Convert outputs to COCO API format
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    print(results)

    detections = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        detections.append({
            "label": model.config.id2label[label.item()],
            "confidence": round(score.item(), 3),
            "box": box
        })
    print(detections)
    return JSONResponse(content=detections)

    # target_sizes = torch.tensor([image.size[::-1]])
    # results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    # detections = []
    # for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    #     box = [round(i, 2) for i in box.tolist()]
    #     detections.append({
    #         "label": model.config.id2label[label.item()],
    #         "confidence": round(score.item(), 3),
    #         "box": box
    #     })
    
    # return JSONResponse(content=detections)

# Run with: uvicorn filename:app --reload

