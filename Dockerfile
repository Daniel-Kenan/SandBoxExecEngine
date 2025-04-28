# Use a slim Python base
FROM python:3.10-slim

# Install FastAPI, Uvicorn and Docker SDK
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the sandbox server code
COPY ./sandbox_server.py ./sandbox_server.py

# Expose and run
EXPOSE 8000
CMD ["uvicorn", "sandbox_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
