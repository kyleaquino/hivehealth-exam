# Board Game Geek Similarity Score API

This API provides an endpoint to calculate the similarity score between two Board Game Geek users based on their top 100 rated games.

## Features

- **Calculate Similarity Score**: Compare the top games of two users and calculate a similarity score.

## Prerequisites

- Python 3.11+
- pip

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv source venv/bin/activate
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Development Server

To start the FastAPI server, run the following command:

```bash
fastapi dev main.py
```

## Endpoints

### Calculate Similarity Score

**Endpoint**: `/calculate-similarity-score`

**Method**: `POST`

**Description**: Calculates the similarity score between two users based on their top 100 games.

**Request Body**:

```json
{ "username1": "user1", "username2": "user2" }
```

**Response**:

```json
{ "similarity_score": 75.00 }`
```

## Testing

To run the tests, use the following command:

```bash
pytest
```

## Logging

The API uses Python's built-in logging module to log information. By default, logs are printed to the console. You can adjust the logging configuration in `main.py` as needed.
