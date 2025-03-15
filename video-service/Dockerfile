FROM python:3.10-slim-buster AS base

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./

# Install runtime dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

EXPOSE 5003

CMD ["python", "src/app.py"]
