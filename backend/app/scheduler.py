import time
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.scraping import main_scraping_process

def scheduled_job():
    """
    The main job to be run by the scheduler.
    """
    print("--- Starting scheduled scraping job ---")
    try:
        main_scraping_process()
        print("--- Scheduled scraping job finished successfully ---")
    except Exception as e:
        print(f"--- Scheduled scraping job failed: {e} ---")

def start_scheduler():
    """
    Starts the APScheduler.
    """
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    
    # Schedule the job to run every week on Monday at 3 AM
    scheduler.add_job(scheduled_job, 'cron', day_of_week='mon', hour=3)
    
    # For testing: run every 5 minutes
    # scheduler.add_job(scheduled_job, 'interval', minutes=5)
    
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")

    try:
        # Keep the script running
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler shut down.")

if __name__ == '__main__':
    start_scheduler()
