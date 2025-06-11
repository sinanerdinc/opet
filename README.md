[![Python CI Workflow Status](https://github.com/sinanerdinc/opet/actions/workflows/ci.yml/badge.svg)](https://github.com/sinanerdinc/opet/actions/workflows/ci.yml)
[![Docker Hub](https://img.shields.io/docker/pulls/sinanerdinc/opet.svg)](https://hub.docker.com/r/sinanerdinc/opet)

## Opet
This project allows you to fetch current fuel prices from https://www.opet.com.tr/.

## Installation
You can install the package using the following command:
```
pip install opet
```

## Usage
You can use the project as a library or via the CLI.

### Library Usage
```python
from opet.api import OpetApiClient

client = OpetApiClient()

print(client.get_provinces())
print(client.get_price("55"))
```

### CLI Usage
You can view fuel prices in JSON format by passing the plate code as a parameter:
```
opet-cli --il 34
```

## Methods
- **get_last_update**: Returns the last update time.
- **get_provinces**: Returns the list of provinces and their codes.
- **price**: Returns fuel prices for a given province code.

## Testing
This project includes unit tests written using `pytest` to ensure code quality and reliability. Tests are automatically run on every code change and on pull requests to the `main` branch via GitHub Actions.

## Docker
You can use the application via Docker. You can build your own image using the Dockerfile:
```
docker build -t opet .
```

Alternatively, you can use the pre-built image from [Docker Hub](https://hub.docker.com/r/sinanerdinc/opet):
```
docker pull sinanerdinc/opet
```

### Running CLI with Docker
To run the CLI using Docker, use the following command:
```
docker run opet cli --il 34
```

### Running API with Docker
To run the API server using Docker, use the following command:
```
docker run -p 8000:8000 opet api
```

This will start the API server on port 8000, and you can access it at `http://localhost:8000`.

You can also map the container's port 8000 to a different port on your host machine:
```
docker run -p 5050:8000 opet api
```
In this case, the API server still runs on port 8000 inside the container, but you can access it at `http://localhost:5050` on your host machine.