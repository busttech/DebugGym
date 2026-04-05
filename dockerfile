FROM python:3.10

WORKDIR /app

COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

# expose port (important for HF)
EXPOSE 7860

# run server (NOT inference)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]