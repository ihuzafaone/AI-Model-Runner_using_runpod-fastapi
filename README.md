# AI Model Runner API

This project provides a FastAPI-based service for running tasks on two different AI models: **Airoboros** and **LLaMA**. The service allows users to submit prompts and retrieve model-generated outputs, with optional tracking of response times. API key authentication is required to use the endpoints.BOth models are deployed on Runpod cloud for AI 

## Features

- **Run tasks on Airoboros and LLaMA models**
- **Stream task output until completion**
- **Time-tracking functionality for tasks**
- **API key-based authentication for requests**

## Requirements

To run this project, ensure you have the following installed:

- Python 3.8+
- FastAPI
- Uvicorn (for running the FastAPI server)
- `requests` library
- `python-dotenv` library

## Environment Variables

You must set the following environment variables in a `.env` file:

- `AIROBOROS_ENDPOINT_ID` - The endpoint ID for the Airoboros model API.
- `AIROBOROS_API_KEY` - API key for authenticating with the Airoboros API.
- `LLAMA_ENDPOINT_ID` - The endpoint ID for the LLaMA model API.
- `LLAMA_API_KEY` - API key for authenticating with the LLaMA API.
- `MY_API_KEY` - A hardcoded API key used to authenticate user requests to the FastAPI service (default: `"digifloat"`).

Example `.env` file:
