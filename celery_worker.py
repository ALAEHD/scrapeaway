from celery import Celery

app = Celery('celery_worker', broker='redis://redis-11521.c3.eu-west-1-1.ec2.redns.redis-cloud.com:11521')

if __name__ == '__main__':
    app.start()