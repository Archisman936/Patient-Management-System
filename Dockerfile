FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

# FastAPI on 8000, Streamlit on 8501
EXPOSE 8000 8501

CMD ["bash", "start.sh"]
