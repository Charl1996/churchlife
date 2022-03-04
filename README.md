# Churchlife

## Installation
1. First, install all the required packages
> pip install -r requirements.txt

2. Celery will be installed among others, but celery requires
a broker service in order to work. This project uses RabbitMQ.

Pull RabbitMQ docker container
> pull container 

Start the service
> start service

3. Start the celery workers and beat
> start them
