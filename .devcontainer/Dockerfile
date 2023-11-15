FROM python:3.8-slim-buster

RUN pip install --upgrade pip

RUN apt update && apt-get install build-essential cmake python3-dev curl -y && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh -s -- -y