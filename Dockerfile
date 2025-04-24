# Step 1: Build frontend
FROM node:20-alpine AS frontend

WORKDIR /app
COPY frontend/ /app/
RUN npm install && npm run build

# Step 2: Setup Python backend
FROM python:3.11-slim

WORKDIR /app

# Copy backend and preprocessing
COPY backend/app /app/app
COPY backend/requirements.txt /app/
# Delete COPY backend/.env /.env for deployment
COPY preprocessing /app/preprocessing
COPY medquad.csv /app/medquad.csv

# Copy built frontend
COPY --from=frontend /app/build /app/frontend

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]