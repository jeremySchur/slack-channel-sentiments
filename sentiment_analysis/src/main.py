from .slack_utils import update_public_channels, get_new_messages
from .postgres import get_channels, update_timestamps, update_avg_sentiments
from .analysis import analyze_sentiments
from time import sleep
import asyncio
import schedule

def job():
    """
        Job to be run on a schedule.
        This function will be called by the scheduler.
    """
    channels = get_channels()

    update_public_channels(channels)

    asyncio.run(get_new_messages(channels))

    update_timestamps(channels)

    analyze_sentiments(channels)

    update_avg_sentiments(channels)

if __name__ == "__main__":
    """
        Main function to run the job on a schedule.
        This function will be called when the script is executed.
    """ 
    job()
    schedule.every(1).days.at("00:00").do(job)  # Schedule the job to run daily at midnight
    while True:
        schedule.run_pending()
        sleep(1)
