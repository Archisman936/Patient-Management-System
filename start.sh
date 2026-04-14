#!/bin/bash

# Start FastAPI in the background on internal port 8000
uvicorn Backend.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on Render's $PORT (defaults to 8501 locally)
streamlit run Frontend/app.py \
  --server.port ${PORT:-8501} \
  --server.address 0.0.0.0 \
  --server.headless true
