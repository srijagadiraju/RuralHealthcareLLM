# backend/Dockerfile
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy backend app code
COPY backend/app /app/app
COPY backend/requirements.txt /app/

# Copy additional directories used by backend
COPY preprocessing /app/preprocessing
COPY medquad.csv /app/medquad.csv

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for FastAPI app
EXPOSE 8000

# Run the FastAPI app with auto-reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]