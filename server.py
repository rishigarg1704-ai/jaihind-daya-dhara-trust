from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import shutil
import json
import os
import uuid

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# create uploads folder
os.makedirs("uploads", exist_ok=True)

DATA_FILE = "data.json"


# -----------------------
# DATA HELPERS
# -----------------------

def read_data():
    if not os.path.exists(DATA_FILE):
        return {
            "members": [],
            "gallery": [],
            "projects": []
        }

    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------
# IMAGE SAVE + RESIZE
# -----------------------

def save_image(upload):

    ext = upload.filename.split(".")[-1]
    filename = str(uuid.uuid4()) + "." + ext
    filepath = "uploads/" + filename

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    try:
        img = Image.open(filepath)
        img.thumbnail((1200, 1200))
        img.save(filepath, optimize=True, quality=85)
    except:
        pass

    return filepath


# -----------------------
# MEMBER
# -----------------------

@app.post("/member")
async def add_member(name: str = Form(...), role: str = Form(...), photo: UploadFile = File(...)):

    filepath = save_image(photo)

    data = read_data()

    data["members"].append({
        "name": name,
        "role": role,
        "image": filepath
    })

    save_data(data)

    return {"status": "member added"}


@app.delete("/delete-member/{index}")
def delete_member(index: int):

    data = read_data()

    if index < len(data["members"]):
        data["members"].pop(index)
        save_data(data)

    return {"status": "member deleted"}


# -----------------------
# GALLERY
# -----------------------

@app.post("/gallery")
async def add_gallery(title: str = Form(...), photo: UploadFile = File(...)):

    filepath = save_image(photo)

    data = read_data()

    data["gallery"].append({
        "title": title,
        "image": filepath
    })

    save_data(data)

    return {"status": "image added"}


@app.delete("/delete-gallery/{index}")
def delete_gallery(index: int):

    data = read_data()

    if index < len(data["gallery"]):
        data["gallery"].pop(index)
        save_data(data)

    return {"status": "gallery deleted"}


# -----------------------
# PROJECT
# -----------------------

@app.post("/project")
async def add_project(title: str = Form(...), description: str = Form(...), photo: UploadFile = File(...)):

    filepath = save_image(photo)

    data = read_data()

    data["projects"].append({
        "title": title,
        "description": description,
        "image": filepath
    })

    save_data(data)

    return {"status": "project added"}


@app.delete("/delete-project/{index}")
def delete_project(index: int):

    data = read_data()

    if index < len(data["projects"]):
        data["projects"].pop(index)
        save_data(data)

    return {"status": "project deleted"}


# -----------------------
# GET DATA
# -----------------------

@app.get("/data")
def get_data():
    return read_data()


# -----------------------
# STATIC FILES
# -----------------------

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")