from dotenv import load_dotenv
import os
load_dotenv("project/.env")


api_key = os.getenv("MISTRAL_API_KEY")

# Verify it loaded correctly
if api_key:
    print("✅ API key loaded successfully")
else:
    print("❌ API key not found. Check your .env file or environment variables.")
    