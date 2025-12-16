
import time
import schedule
from tier1_data_pipeline.fetch_macro import run_fetch_macro
from tier1_data_pipeline.fetch_geopolitics import run_fetch_geopolitics
from tier1_data_pipeline.fetch_sentiment import run_fetch_sentiment

def daily_job():
    print("--- Starting Daily Data Pipeline ---")
    try:
        run_fetch_macro()
        run_fetch_geopolitics()
        run_fetch_sentiment()
        print("--- Daily Data Pipeline API Completed ---")
    except Exception as e:
        print(f"Pipeline Error: {e}")

# Call immediately for testing purposes
if __name__ == "__main__":
    daily_job()
    # schedule.every().day.at("09:00").do(daily_job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
