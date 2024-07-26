# BGG User Comparison API

This project provides a FastAPI-based web service that calculates the similarity score between the top 100 rated games of two Board Game Geek (BGG) users. The service fetches users' game collections and determines the overlap in their top-rated games.

## Table of Contents

- [BGG User Comparison API](#hivehealth-exam)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Run the Application](#run-the-application)
    - [API Endpoint](#api-endpoint)
  - [Directory Structure](#directory-structure)
  - [Logging](#logging)
  - [Testing](#testing)

## Features

- Fetches top 100 rated games for a BGG user.
- Computes similarity score between two users based on their top-rated games.
- Logs detailed information about the API requests and errors.

## Requirements

- Python 3.11+
- FastAPI
- Requests
- Uvicorn

## Installation

1. Clone the repository:

   ```bash
   https://github.com/kyleaquino/hivehealth-exam.git
   cd hivehealth-exam
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the Application

To start the FastAPI server, run the following command:

```bash
fastapi dev main.py
```

### API Endpoint

#### Calculate Similarity Score

- **URL**: `/calculate-similarity-score`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:

  ```json
  {
    "username1": "user1",
    "username2": "user2"
  }
  ```

- **Response**:

  ```json
  {
    "similarity_score": "0.75"
  }
  ```

You can test the endpoint using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/calculate-similarity-score" -H "Content-Type: application/json" -d '{"username1": "user1", "username2": "user2"}'
```

## Directory Structure

```
hivehealth-exam/
│
├── main.py
├── requirements.txt
├── .pylintrc
├── .gitignore
├── README.md
├── logs/
├── scripts/
│   └── bgg_compare_users.py
|   └── README.md
├── services/
│   └── bgg_service.py
|   └── README.md
└── tests/
    └── test_bgg_service.py
|   └── README.md
```

Important Files:

- **main.py**: The main FastAPI application.
- **requirements.txt**: Project dependencies.
- **services/bgg_service.py**: Contains classes and methods to interact with the BGG XML API.
- **scripts/bgg_compare_users.py**: A script to compare two users' game tastes from the command line.
- **tests/test_bgg_service.py**: Unit tests for the `bgg_service` module.

## Logging

Logging is configured to output debug-level logs to `logs/app.log`. Logs include timestamps, log levels, and messages.

## Testing

Unit tests are located in the `tests` directory. To run the tests, use:

```bash
pytest
```
