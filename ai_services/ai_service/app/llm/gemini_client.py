# import os
# from google import genai
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")

# if not API_KEY:
#     raise RuntimeError("GEMINI_API_KEY is missing")

# genai.configure(api_key=API_KEY)

# model = genai.GenerativeModel("models/gemini-pro")



# def generate_response(prompt: str) -> str:
#     response = model.generate_content(prompt)
#     return response.text



import os
from dotenv import load_dotenv
from google import genai
from fastapi import HTTPException

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models = client.models.list()
for m in models:
    print(m.name)


def generate_response(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini upstream failure: {str(e)}"
        )



