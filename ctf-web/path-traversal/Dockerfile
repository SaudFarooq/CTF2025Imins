FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py files/ secret/ ./
RUN echo "CH{traversal_reads_secret}" > secret/flag.txt
EXPOSE 8000
CMD ["python", "app.py"]
