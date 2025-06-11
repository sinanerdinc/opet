FROM python:3.12-alpine
LABEL maintainer="Sinan Erdinc <hello@sinanerdinc.com>"

WORKDIR /app

# Suppress all Python warnings
ENV PYTHONWARNINGS=ignore

# Copy entire project
COPY . /app/

# Install uv and create virtual environment
RUN pip install uv
RUN uv venv

# Install dependencies and package
RUN uv pip install --system -r requirements.txt
RUN pip install .

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["cli"]
