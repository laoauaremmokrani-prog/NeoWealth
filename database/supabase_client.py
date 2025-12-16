
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', '.env'))

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL and Key must be set in the .env file")

supabase: Client = create_client(url, key)

def get_client() -> Client:
    return supabase
