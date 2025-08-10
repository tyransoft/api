from django_apscheduler.jobstores import register_events,DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from .models import Subscription

def scheduler_job():
    today=now().date()
    sub=Subscription.objects.filter(end_date__lte=today,is_active=True)
    for i in sub:
        i.is_active=False
        i.save()

def start():
    job=BackgroundScheduler()
    job.add_jobstore(DjangoJobStore(),"default")
    job.add_job(scheduler_job,trigger='cron',hour=2,minute=0,id='deactive_subs',replace_existing=True)
    register_events(job)
    job.start()        