
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import json
from datetime import datetime

from pathlib import Path

# Load environment variables from .env file in backend directory
backend_dir = Path(__file__).parent
load_dotenv(dotenv_path=backend_dir / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class SupabaseDB:
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase URL and Key must be set in environment variables.")
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def fetch_latest_tier1_data(self):
        """Fetch the latest record from tier1_raw."""
        try:
            response = self.client.table("tier1_raw").select("*").order("created_at", desc=True).limit(1).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching Tier 1 data: {e}")
            return None

    def upload_tier1_data(self, data: dict):
        """Upload data to tier1_raw."""
        try:
            # Ensure timestamp
            if "created_at" not in data:
                data["created_at"] = datetime.utcnow().isoformat()
            self.client.table("tier1_raw").insert(data).execute()
            print("Successfully uploaded to tier1_raw")
        except Exception as e:
            print(f"Error uploading to tier1_raw: {e}")
            raise

    def fetch_latest_tier2_data(self):
        """Fetch the latest record from tier2_processed."""
        try:
            response = self.client.table("tier2_processed").select("*").order("created_at", desc=True).limit(1).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching Tier 2 data: {e}")
            return None

    def upload_tier2_data(self, data: dict):
        """Upload data to tier2_processed."""
        try:
            if "created_at" not in data:
                data["created_at"] = datetime.utcnow().isoformat()
            self.client.table("tier2_processed").insert(data).execute()
            print("Successfully uploaded to tier2_processed")
        except Exception as e:
            print(f"Error uploading to tier2_processed: {e}")
            raise

    def fetch_historical_tier2_data(self, limit: int = 365):
        """Fetch historical records from tier2_processed for backtesting."""
        try:
            # Fetch essential columns for backtesting
            response = self.client.table("tier2_processed").select("*").order("created_at", desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []

    def save_prediction(self, prediction_data: dict):
        """Save prediction result to predictions table."""
        try:
            if "created_at" not in prediction_data:
                prediction_data["created_at"] = datetime.utcnow().isoformat()
            self.client.table("predictions").insert(prediction_data).execute()
            print("Successfully saved prediction")
        except Exception as e:
            print(f"Error saving prediction: {e}")
            # Don't raise here to avoid blocking response? 
            # Better to log.

# Singleton instance
try:
    db = SupabaseDB()
except ValueError:
    db = None
