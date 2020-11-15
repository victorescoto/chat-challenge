from app.commands import StockCommand
from app.services import RabbitMQService


class Chatbot:
    def __init__(self):
        self.message_broker = RabbitMQService()

    def callback(self, ch, method, properties, body):
        command, params = body.decode("utf-8").split(":")
        if command == StockCommand.name:
            StockCommand().resolve(params)
        ch.basic_ack(method.delivery_tag)

    def run(self):
        self.message_broker.consume(self.callback)


if __name__ == "__main__":
    Chatbot().run()
