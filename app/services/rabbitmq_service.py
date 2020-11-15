import os

import pika


class RabbitMQService:
    def __init__(self, queue=None):
        if not queue:
            queue = os.environ.get("RABBITMQ_QUEUE")

        self.user = os.environ.get("RABBITMQ_USER")
        self.password = os.environ.get("RABBITMQ_PASS")
        self.host = os.environ.get("RABBITMQ_HOST")
        self.port = os.environ.get("RABBITMQ_PORT")
        self.queue_name = queue

    def run(self):
        credentials = pika.credentials.PlainCredentials(self.user, self.password)
        conn_parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=credentials, virtual_host="/"
        )
        self.connection = pika.BlockingConnection(conn_parameters)
        self.channel = self.connection.channel()
        self.set_queue()

        return self

    def set_queue(self, queue_name=None):
        self.queue = self.channel.queue_declare(
            self.queue_name if not queue_name else queue_name, durable=True
        )

    def close(self):
        self.connection.close()

    def read(self):
        method_frame, _, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            return {"body": body.decode("utf-8")}
        return None

    def consume(self, callback):
        self.run()
        self.channel.basic_consume(self.queue_name, callback)
        self.channel.start_consuming()

    def send(self, msg):
        return self.channel.basic_publish("", self.queue.method.queue, msg)
