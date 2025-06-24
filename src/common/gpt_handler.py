import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT="https://models.github.ai/inference"
MODEL = "openai/gpt-4.1"

def create_prompt(prompt_file, notes=""):
    with open(f"src/common/prompts/{prompt_file}.txt", "r") as file:
        prompt = file.read()
    return prompt.format(notes=notes)

def generate_response(notes):
    prompt = create_prompt("summarize_notes", notes)
    client = ChatCompletionsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(GITHUB_TOKEN),
    )

    response = client.complete(
        messages=[
            SystemMessage(""),
            UserMessage(prompt),
        ],
        temperature=1,
        top_p=1,
        model=MODEL
    )

    return response.choices[0].message.content