from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(refresh_function):

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        refresh_function,
        "cron",
        hour=2,
        minute=0
    )

    scheduler.start()

    return scheduler