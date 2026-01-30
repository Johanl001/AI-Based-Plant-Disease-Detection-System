# Backend
FROM python:3.9-slim as backend

WORKDIR /app/backend

# Install system dependencies for OpenCV/Pillow
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY model/ /app/model/

# Frontend
FROM node:18-alpine as frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Final Stage (Serving both or setting up structure - typically we serve backend and frontend separately or backend serves static files)
# For this "end to end app", a common pattern is FastApi serves the React build.

FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

COPY --from=backend /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend /app/backend /app/backend
COPY --from=backend /app/model /app/model
COPY --from=frontend /app/frontend/dist /app/frontend/dist

WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
