# Development Report

## Overview

This report provides an overview of the approach taken to develop the BGG User Comparison API, which includes creating a Python library wrapper for the BGG XML API, building a FastAPI application to compare users' top-rated games, and writing unit tests to ensure the reliability of the implemented functionality.

## Approach

### Step 1: Create Python Library Wrapper for BGG XML API

#### Implementation

1. **BGGClient**:
    - A base class to interact with the BGG XML API, handling API requests and parsing XML responses.
    - Implemented retry logic to handle the 202 (Accepted) status, which indicates the request is being processed.

2. **BGGUser**:
    - A class to fetch and parse user information from the BGG API, including optional buddies, guilds, hot list, and top list data.
    - Used helper methods to extract and store user details and lists into respective attributes.

3. **BGGCollectionItem**:
    - A class to fetch and parse the user's game collection.
    - Implemented methods to handle the conversion of XML data into Python objects for easy manipulation.

### Step 2: Develop FastAPI Application

#### Implementation

1. **main.py**:
    - Created a FastAPI application with an endpoint to calculate the similarity score between two BGG users based on their top-rated games.
    - Implemented logging to record API requests and errors.
    - Used Pydantic models for request validation.

2. **Endpoint**:
    - **`/calculate-similarity-score`**: Accepts two BGG usernames and calculates the similarity score between their top 100 rated games.

### Step 3: Write Unit Tests

#### Implementation

1. **tests/test_bgg_service.py**:
    - Used `unittest` and `unittest.mock` to create mock responses and test the functionality of `BGGClient`, `BGGUser`, and `BGGCollectionItem`.
    - Verified that the XML parsing and API interactions worked as expected.

## Improvements

### If More Time Was Available

1. **Enhanced Error Handling**:
    - Implement more granular error handling for different types of HTTP errors and response scenarios.
    - Provide more detailed error messages and possibly retry mechanisms for transient errors.

2. **Caching**:
    - Implement caching for API responses to reduce the number of requests to the BGG API, especially for frequently requested data.
    - Use an in-memory cache (e.g., Redis) to store results temporarily.

3. **Pagination Support**:
    - Extend the library to handle pagination for buddies and guilds lists properly.
    - Fetch and aggregate all pages of data if necessary.

4. **Asynchronous Requests**:
    - Convert the synchronous API requests to asynchronous using `httpx` or `aiohttp` for improved performance, especially when fetching data for multiple users.

5. **Data Validation and Enrichment**:
    - Add more data validation to ensure the integrity of the fetched data.
    - Enrich the response with additional data from other sources or APIs if available.

6. **More Comprehensive Tests**:
    - Write additional unit tests to cover edge cases and error scenarios.
    - Implement integration tests to test the end-to-end functionality of the FastAPI application.

7. **Documentation**:
    - Improve documentation with detailed descriptions of each class and method.
    - Provide usage examples and API documentation using tools like Swagger or ReDoc integrated with FastAPI.


## Bonus Task: Create Another Endpoint

I didnt pursue this task since im not sure how to properly approach the problem efficiently

### Proposed Steps to Create an Endpoint to Find Similar Users

1. **Extend the Service Layer**:
    - Add a new method in the `BGGCollectionItem` class to fetch a list of usernames with similar game tastes.
    - This method can either fetch a predefined list of users or store a subset of user data in a local SQLite database for efficient querying.

2. **Create a New Endpoint**:
    - In `main.py`, add a new endpoint `/find-similar-users`.
    - This endpoint should accept a username and return a list of usernames with similar tastes.

3. **Implement the Logic to Compare Users**:
    - Fetch the top games for the given username.
    - Compare these games with the top games of other users to calculate similarity scores.
    - Return the list of users with the highest similarity scores.

### Considerations for Step 1 I have trouble choosing between.

1. **Predefined List**:
    - Suitable for initial testing and smaller datasets.
    - Easy to implement but may not scale well with a large number of users.
    - Example: A static list of usernames for quick comparisons.

2. **Local Database**:
    - Better for larger datasets and more efficient querying.
    - Requires additional setup and data management.
    - Allows for more dynamic and scalable comparisons.
    - Example: Use SQLite to store and query user game collections.
