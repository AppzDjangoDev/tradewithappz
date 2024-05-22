from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from django.test import RequestFactory
from fyersapi.views import get_data_instance

logger = logging.getLogger(__name__)

def my_scheduled_task():
    logger.info("Scheduled task is running.")
    try:
        # Create a fake request object
        factory = RequestFactory()
        request = factory.get('/fake-path/')
        
        # Call your function with the request object
        data_instance = get_data_instance(request)
        fund_data = data_instance.funds()
        logger.info(f"Data instance: {fund_data}")
    except Exception as e:
        logger.error(f"Error running scheduled task: {e}")



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_scheduled_task, CronTrigger(hour=11, minute=25))
    scheduler.start()
    logger.info("Scheduler started.")

    # Shut down the scheduler when exiting the app
    import atexit
    atexit.register(lambda: scheduler.shutdown())
