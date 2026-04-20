import os
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime

from agent import agent

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")


@app.post("/query")
async def handle_query(file: UploadFile = File(...), query: str = Form(...)):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, local_filename)

    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format.")

        data_summary = {
            "current_file": local_filename,
            "columns": df.columns.tolist(),
            "shape": df.shape,
        }

        result = await agent.run(
            f"File Context: {data_summary}\nUser Request: {query}",
            deps={"df": df, "path": file_path},
        )

        return {"response": result.output, "filename": local_filename}

    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path, filename=filename, media_type="application/octet-stream"
        )
    raise HTTPException(status_code=404, detail="File not found")
