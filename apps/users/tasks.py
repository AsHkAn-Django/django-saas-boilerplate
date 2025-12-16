from celery import shared_task
import time

@shared_task
def simulate_heavy_scraping(user_email):
    """
    Simulates a heavy background task (like scraping data).
    """
    print(f" Starting scraping job for {user_email}...")

    time.sleep(10)

    print(f"Finished scraping job for {user_email}!")
    return "Data Scraped Successfully"
