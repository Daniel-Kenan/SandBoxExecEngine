import os
import uuid
import shutil
import docker                                          # Docker SDK for Python :contentReference[oaicite:13]{index=13}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from docker.errors import APIError

app = FastAPI()
client = docker.from_env()

class CodeRequest(BaseModel):
    lang: str
    code: str

@app.post("/run")
async def run_code(req: CodeRequest):
    # create a unique working directory
    workdir = f"/tmp/{uuid.uuid4()}"
    os.makedirs(workdir)

    # write code to file
    if req.lang == "python":
        filename = "script.py"
        cmd = ["python", f"/sandbox/{filename}"]
    elif req.lang == "c":
        filename = "prog.c"
        cmd = ["bash", "-c", "gcc prog.c -o prog && ./prog"]
    elif req.lang == "javascript":
        filename = "script.js"
        cmd = ["node", f"/sandbox/{filename}"]
    elif req.lang == "bash":
        filename = "script.sh"
        cmd = ["bash", f"/sandbox/{filename}"]
    elif req.lang == "pwsh":
        filename = "script.ps1"
        cmd = ["pwsh", f"/sandbox/{filename}"]
    else:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # write the submitted code
    with open(os.path.join(workdir, filename), "w") as f:
        f.write(req.code)

    # run the container
    image_map = {
        "python": "python:3.10-slim",
        "c": "gcc:latest",
        "javascript": "node:16-slim",
        "bash": "debian:stable-slim",
        "pwsh": "mcr.microsoft.com/powershell:latest",
    }
    try:
        output = client.containers.run(
            image=image_map[req.lang],
            command=cmd,
            volumes={workdir: {'bind': '/sandbox', 'mode': 'rw'}},
            network_disabled=True,
            auto_remove=True,
            stderr=True,
            stdout=True,
            working_dir="/sandbox",
            detach=False,
            stdout=True,
            stderr=True,
        )
        # clean up
        shutil.rmtree(workdir, ignore_errors=True)
        return {"output": output.decode()}
    except APIError as e:
        shutil.rmtree(workdir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))
