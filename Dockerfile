# Use a slim Python base
FROM python:3.10-slim                              # official Python image :contentReference[oaicite:10]{index=10}

# Install FastAPI, Uvicorn and Docker SDK
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt    # best practice for Dockerfiles :contentReference[oaicite:11]{index=11}

# Copy the sandbox server code
COPY sandbox_server.py .

# Expose and run
EXPOSE 8000
CMD ["uvicorn", "sandbox_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
