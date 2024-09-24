from fastapi import FastAPI, HTTPException, Header, Depends
from dotenv import load_dotenv
import os
import requests
from time import sleep, time
import logging

# Load environment variables from the .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Environment variables for the two models
AIROBOROS_ENDPOINT_ID = os.environ.get("AIROBOROS_ENDPOINT_ID")
AIROBOROS_API_KEY = os.environ.get("AIROBOROS_API_KEY")
AIROBOROS_URI = f"https://api.runpod.ai/v2/{AIROBOROS_ENDPOINT_ID}/run"

LLAMA_ENDPOINT_ID = os.environ.get("LLAMA_ENDPOINT_ID")
LLAMA_API_KEY = os.environ.get("LLAMA_API_KEY")
LLAMA_URI = f"https://api.runpod.ai/v2/{LLAMA_ENDPOINT_ID}/run"

# valid API key for user authenticatio
VALID_API_KEY = os.environ.get("MY_API_KEY")  


def verify_api_key(x_api_key: str = Header()):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")


# Function to run the task for a specific model
def run_task(prompt: str, model: str):
    request = {
        'prompt': prompt,
        'max_new_tokens': 500,
        'temperature': 0.3,
        'top_k': 50,
        'top_p': 0.7,
        'repetition_penalty': 1.2,
        'batch_size': 8,
        'stop': ['</s>']
    }

    if model == 'airoboros':
        URI = AIROBOROS_URI
        API_KEY = AIROBOROS_API_KEY
    elif model == 'llama':
        URI = LLAMA_URI
        API_KEY = LLAMA_API_KEY
    else:
        raise HTTPException(status_code=400, detail="Invalid model specified")

    response = requests.post(URI, json={"input": request}, headers={
        "Authorization": f"Bearer {API_KEY}"
    })

    if response.status_code == 200:
        data = response.json()
        task_id = data.get('id')
        return task_id
    else:
        logging.error(response.json())
        raise HTTPException(status_code=response.status_code, detail="Failed to start task")


# Function to stream output of the task for a specific model
def stream_output(task_id: str, model: str):
    try:
        if model == 'airoboros':
            endpoint_id = AIROBOROS_ENDPOINT_ID
            API_KEY = AIROBOROS_API_KEY
        elif model == 'llama':
            endpoint_id = LLAMA_ENDPOINT_ID
            API_KEY = LLAMA_API_KEY
        else:
            raise HTTPException(status_code=400, detail="Invalid model specified")

        url = f"https://api.runpod.ai/v2/{endpoint_id}/status/{task_id}"
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        while True:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'COMPLETED':
                    return data['output']
            elif response.status_code >= 400:
                logging.error(response.json())
                raise HTTPException(status_code=response.status_code, detail="Error fetching task status")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def home():
    return "API is running"

# Endpoint to run a task on Airoboros model
@app.post("/run-task/airoboros/")
def run_airoboros_task(prompt: str, x_api_key: str = Depends(verify_api_key)):
    task_id = run_task(prompt, model='airoboros')
    output = stream_output(task_id, model='airoboros')
    return {"output": output}


# Endpoint to run a task on LLaMA model
@app.post("/run-task/llama/")
def run_llama_task(prompt: str, x_api_key: str = Depends(verify_api_key)):
    task_id = run_task(prompt, model='llama')
    output = stream_output(task_id, model='llama')
    return {"output": output}


# Timed task endpoint for Airoboros model
@app.post("/timed-task/airoboros/")
def timed_airoboros_task(prompt: str, x_api_key: str = Depends(verify_api_key)):
    start_time = time()  # Start timer
    task_id = run_task(prompt, model='airoboros')
    output = stream_output(task_id, model='airoboros')
    end_time = time()  # End timer
    elapsed_time = end_time - start_time
    return {"output": output, "response_time_seconds": elapsed_time}


# Timed task endpoint for LLaMA model
@app.post("/timed-task/llama/")
def timed_llama_task(prompt: str, x_api_key: str = Depends(verify_api_key)):
    start_time = time()  # Start timer
    task_id = run_task(prompt, model='llama')
    output = stream_output(task_id, model='llama')
    end_time = time()  # End timer
    elapsed_time = end_time - start_time
    return {"output": output, "response_time_seconds": elapsed_time}

