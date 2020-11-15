import csv
import json

import time

import requests

from ..services import RabbitMQService


class StockCommand:
    name = "stock"

    def __init__(self) -> None:
        self.message_broker = RabbitMQService()

    def send_to_queue(self, message, room):
        stock_code = message.split("=")[-1]

        self.message_broker.run()
        self.message_broker.set_queue("chat_commands")
        self.message_broker.send(f"{self.name}:{stock_code};{room}")

    def resolve(self, params):
        stock_code, room = params.split(";")

        with requests.Session() as s:
            download = s.get(
                f"https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcv&h&e=csv"
            )
            decoded_content = download.content.decode("utf-8")

            csv_content = csv.reader(decoded_content.splitlines(), delimiter=",")
            csv_content_as_list = list(csv_content)
            csv_content_as_dict = dict(
                zip(csv_content_as_list[0], csv_content_as_list[1])
            )

        payload = json.dumps(
            {
                "message": {
                    "content": f"{csv_content_as_dict['Symbol']} quote is ${csv_content_as_dict['Close']} per share",
                    "createdAt": time.strftime("%Y-%M-%d %H:%M:%S"),
                    "author": {"id": 0, "username": "Chatbot"},
                },
                "room": room,
            }
        )
        self.message_broker.run()
        self.message_broker.set_queue("chat_messages")
        self.message_broker.send(payload)
