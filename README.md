# CodeReviewAI

## Introduction




## Features
- **Gemini API Integration**: Performs code analysis and generates reviews.
- **GitHub API Integration**: Fetches repository contents for review.
- **Asynchronous Programming**: Improves performance for external API calls.
- **API Rate Limits**: asyncio.Semaphore
- **Error Handling & Logging**: Manages API errors and ensures traceable logging.
- **Test Coverage**: Includes unit tests with pytest and httpx.
- **Caching**: Utilizes Redis with TTL mechanism for improved performance.
- **Validation**: Use Pydantic for input validation
- **Containerization**: Docker for easy deployment


## Setup Instructions

### Clone the Repository:

```bash
    git clone git@github.com:Nik-Bz-22/CodeReviewAI.git
    cd CodeReviewAI
```

### .ENV
**Create .env file in the root of the project using the .env.example template.**

## Important Notice!

**Since the Gemini API is restricted in certain regions (see the list of available countries [here](https://ai.google.dev/gemini-api/docs/available-regions)), you need to enable a VPN before running the application to ensure it works correctly.**

### Start with Docker
```bash
   make docker-up
```

### Local start
#### Install Dependencies: Using poetry:
```bash
    poetry install
```

#### Run Redis (with Docker for example)
```bash
   docker compose up redis
```

#### Run app

```bash
    make run
```

## Usage

### POST /review

#### Request Body:
    assignment_description (string): A description of the coding assignment.
    github_repo_url (string): The URL of the GitHub repository to review.
    candidate_level (string): The experience level (Junior, Middle or Senior).


### Example

#### Request
POST / http://localhost:8000/review/


#### Response
```python
{
    "review": {
        "files": [
            "example.py",
            "example.js",
            "example.cpp",
            "etc..."
            
        ],
        "downsides": [
            "First downsides",
            "Second downsides",
            "One more downsides",
            "etc..."
            
        ],
        "comments": [
            "Several comments",
            "One more",
            "etc..."
            
        ],
        "rating": 7,
        "conclusion": "Some conclusion about project"
    }
}
```
### Testing and Code Coverage  

To check the percentage of code covered by tests, run the following command:  

```bash  
    make coverage  
```

## What-if part:
To reduce memory usage, it’s possible to use two or more Redis databases. With such a decomposition, it will be possible to add a time-to-live (TTL) for each repository analysis individually, rather than applying it to the entire repository at once. 

Additionally, a task manager like Celery can be used for background asynchronous data processing. Regarding the limitations on GitHub API usage, I’ve resolved this by using an asyncio Semaphore to limit the number of simultaneous requests and handle them efficiently. This approach helps avoid overloading both their API and the application’s own memory. 

I also think it would be a good idea to split this into two microservices: one responsible for fetching data from GitHub and the other for interacting with the AI.
