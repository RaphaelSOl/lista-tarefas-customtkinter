FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-tk xvfb && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY lista_tarefas_customtkinter.py .

CMD ["xvfb-run", "-a", "python", "lista_tarefas_customtkinter.py"]