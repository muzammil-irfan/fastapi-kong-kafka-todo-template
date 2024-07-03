
# FastAPI-Kong-Kafka-Todo-Template

A template project integrating FastAPI, Kong API Gateway, and Kafka, orchestrated with Docker Compose for a todo application.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is a template for building applications with FastAPI, Kong API Gateway, and Kafka, managed with Docker Compose. It includes a basic todo application to demonstrate the integration.

## Features

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Kong API Gateway**: An open-source API Gateway and Microservices Management Layer, delivering high performance and reliability.
- **Kafka**: A distributed streaming platform that is used to build real-time data pipelines and streaming apps.
- **Docker Compose**: A tool for defining and running multi-container Docker applications.

## Architecture

![Architecture Diagram](path/to/architecture-diagram.png)

## Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the repository**:
   \`\`\`bash
   git clone https://github.com/your-username/fastapi-kong-kafka-todo-template.git
   cd fastapi-kong-kafka-todo-template
   \`\`\`

2. **Start the services**:
   \`\`\`bash
   docker-compose up -d
   \`\`\`

3. **Check the logs** (optional):
   \`\`\`bash
   docker-compose logs -f
   \`\`\`

### Configuration

- **Kong**: Configuration files for services and routes can be found in `kong.yaml`.
- **FastAPI**: The FastAPI application is located in the `app` directory.
- **Kafka**: Kafka configurations are in `docker-compose.yaml`.

## Usage

- Access the FastAPI application at `http://localhost:8000`.
- Kong Admin API is available at `http://localhost:8001`.
- Kong Proxy is available at `http://localhost:8000`.

### Accessing the Todo API

- **Get Todos**: `GET /todos`
- **Create Todo**: `POST /todos`
- **Update Todo**: `PUT /todos/{id}`
- **Delete Todo**: `DELETE /todos/{id}`

## Endpoints

Detailed API documentation is available via Swagger UI at `http://localhost:8000/docs`.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
