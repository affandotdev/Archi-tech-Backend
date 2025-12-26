# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")

# try:
#     client = genai.Client(api_key=API_KEY)
#     candidates = [
#         "models/gemini-1.5-flash",
#         "models/gemini-1.5-pro",
#         "models/gemini-2.0-flash-exp",
#         "models/gemini-2.0-flash",
#         "models/gemini-pro",
#         "models/gemini-1.0-pro"
#     ]
    
#     print("Testing models...")
#     for model_name in candidates:
#         print(f"Trying {model_name}...")
#         try:
#             response = client.models.generate_content(
#                 model=model_name,
#                 contents="Hello"
#             )
#             print(f"SUCCESS with {model_name}!")
#             with open("success.txt", "w") as f:
#                 f.write(model_name)
#             break
#         except Exception as e:
#             print(f"Failed {model_name}: {e}")
# except Exception as e:
#     print(f"Error listing models: {e}")
