from google import genai
from decouple import config
client = genai.Client(api_key=config("GEMINI_API_KEY"))

response = client.models.generate_content(model="gemini-2.5-flash",contents="Explain React in one sentence")

print(response.text)
