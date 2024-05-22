from django_cron import CronJobBase, Schedule
from datetime import datetime

class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['10:16']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'fyersapi.my_cron_job'  # a unique code

    def do(self):
        # Your task here
        print(f'Cron job running at {datetime.now()}')
        # For example, sending an email, updating database, etc.

