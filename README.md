
# PaperRetrievalService

This is a Flask-based microservice designed to retrieve academic papers from various sources such as Arxiv using multiple retrievers. The service can be easily deployed using Docker and Docker Compose.

## Features

- Retrieve academic papers from sources like Arxiv.
- Modular retriever architecture.
- REST API for retrieving papers based on search queries and date ranges.
- Dockerized for easy deployment.
- **Dynamic Configuration of Retrievers**: Add or modify retrievers using a JSON configuration file.

## Project Structure

```
PaperRetrievalService
├── app
│   ├── __init__.py
│   ├── routes.py
├── Dockerfile
├── libs
│   └── PaperRetrievalService
│       ├── arxiv_retriever.py
│       ├── base_retriever.py
│       └── retriever_manager.py
├── main.py
├── libs
│   └── paper_retrieval.log
└── retrievers_config.json
```

## Requirements

Make sure you have the following installed:
- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/PaperRetrievalService.git
cd PaperRetrievalService
```

### 2. Build and Run the Service with Docker Compose

Build and start the service using Docker Compose:

```bash
docker-compose up --build
```

This will:
- Build the Docker image for the Flask app.
- Start the Flask app on port `5502`.

### 3. Access the Service

Once the service is running, you can access it at:

```
http://localhost:5502
```

### 4. API Usage

#### POST `/retrieve_papers`

Retrieve papers from all configured retrievers.

**Request Body:**
```json
{
  "fields_to_search": ["cryptography", "algorithms"],
  "output_dir": "./downloaded_papers",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

**Response:**
```json
{
  "message": "Papers retrieved successfully",
  "files": [
    "./downloaded_papers/paper1.pdf",
    "./downloaded_papers/paper2.pdf"
  ]
}
```

### 5. Dynamic Configuration of Retrievers

Retrievers are configured dynamically through the `retrievers_config.json` file. You can easily add new retrievers by modifying this configuration without changing the main code.

#### Example of `retrievers_config.json`:

```json
{
  "retrievers": {
    "arxiv": "libs.PaperRetrievalService.arxiv_retriever.ArxivRetriever",
    "other": "libs.PaperRetrievalService.other_retriever.OtherRetriever"
  }
}
```

- Each retriever is represented as a key-value pair where:
  - The **key** is the name of the retriever (e.g., `arxiv`).
  - The **value** is the path to the Python class responsible for implementing the retriever logic.

- To add a new retriever:
  1. Implement the retriever class.
  2. Add it to the `retrievers_config.json` file.

### 6. Stop the Service

To stop the Docker containers:

```bash
docker-compose down
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
