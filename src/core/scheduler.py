from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def set_jobs():

    scheduler.start()


async def stop_scheduler():
    scheduler.shutdown()
