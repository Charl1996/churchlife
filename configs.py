from secrets import *

APPLICATION_HOST = '127.0.0.1'
APPLICATION_PORT = 8082

DEFAULT_MESSENGER_HANDLER = 'respondio'

# RabbitMQ broker service
RABBIT_PORT = 5672
BROKER_URL = f'amqp://{RABBIT_USER}:{RABBIT_PASS}@localhost:{RABBIT_PORT}//'
