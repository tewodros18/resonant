import asyncio
import json
import os
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse



app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/audio")
async def serve_audio_file(directory):
    """Serve audio files from media directory"""
    params = directory.split('-')
    file_path = os.path.join(f"./static/{params[0]}/{params[1]}.wav")
    
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(file_path, media_type="audio/wav")

@app.get("/images")
async def get_images():
    names_list = []
    painting_names = []
    for file in os.listdir("./static/"):
        path = os.path.join(f"./static/{file}/{file}.json")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "artistDisplayName" in data and isinstance(data["artistDisplayName"], str):
                names_list.append(data["artistDisplayName"])
            if "title" in data and isinstance(data["title"], str):
                painting_names.append(data["title"])
    
    return JSONResponse(content={"names": names_list, "painting_names": painting_names})