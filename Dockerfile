FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

COPY pyproject.toml .
RUN pip install .

COPY src/ ./src/

ENV PYTHONPATH=/app/src