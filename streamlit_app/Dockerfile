FROM python:3.11-slim

WORKDIR /ui

COPY streamlit_app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY streamlit_app /ui

CMD ["streamlit", "run", "signup.py", "--server.port=8501", "--server.address=0.0.0.0"]
