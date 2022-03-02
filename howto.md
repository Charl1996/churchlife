# General How-to's


## Celery

### Start celery worker
> celery -A <celery-file> worker

In this case this becomes
> celery -A celery_service worker


### Kill all celery processes
> kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n' ' ') > /dev/null 2>&1


## RabbitMQ

Start container with name, username and password
> docker run --name <container-name> -e RABBITMQ_DEFAULT_USER=<username> -e RABBITMQ_DEFAULT_PASS=<user-pass> -p <port>:5672 rabbitmq
