import logging
import uuid
from enum import Enum
from typing import Union

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from . import models

logger = logging.getLogger(__name__)


class Events(Enum):
    INTERNAL_DEPOSIT_CONFIRMED = "internal.deposit.confirmed"
    BLOCKCHAIN_BLOCK_CREATED = "blockchain.block.created"
    BLOCKCHAIN_DEPOSIT_RECEIVED = "blockchain.deposit.received"
    BLOCKCHAIN_DEPOSIT_BROADCAST = "blockchain.deposit.broadcast"
    BLOCKCHAIN_DEPOSIT_CONFIRMED = "blockchain.deposit.confirmed"
    BLOCKCHAIN_ROUTE_EXPIRED = "blockchain.payment_route.expired"
    ETHEREUM_NODE_UNAVAILABLE = "ethereum_node.unavailable"
    ETHEREUM_NODE_OK = "ethereum_node.ok"
    RAIDEN_ROUTE_EXPIRED = "raiden.payment_route.expired"
    RAIDEN_DEPOSIT_RECEIVED = "raiden.deposit.received"
    RAIDEN_DEPOSIT_CONFIRMED = "raiden.deposit.confirmed"


def accept_subprotocol(consumer):
    try:
        subprotocol = consumer.scope["subprotocols"][0]
        consumer.accept(subprotocol)
    except IndexError:
        consumer.accept()


class SessionEventsConsumer(JsonWebsocketConsumer):
    @classmethod
    def get_group_name(cls, session_key: str) -> str:
        return f"events.{session_key}"

    def connect(self):
        session = self.scope["session"]
        session.save()
        accept_subprotocol(self)
        group_name = self.__class__.get_group_name(session.session_key)
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
        logger.debug(f"Session Event consumer {group_name} connected")

    def notify_event(self, message):
        logger.info(f"Message received: {message}")
        message.pop("type", None)
        event = message.pop("event", "notification")
        logger.debug(f"Sending {event} notification... {message}")

        self.send_json({"event": event, "data": message})


class CheckoutConsumer(JsonWebsocketConsumer):
    @classmethod
    def get_group_name(cls, checkout_id: Union[uuid.UUID, str]) -> str:
        uid = uuid.UUID(str(checkout_id))
        return f"checkout.{uid.hex}"

    def connect(self):
        checkout_id = self.scope["url_route"]["kwargs"].get("pk")

        if not models.Checkout.objects.filter(id=checkout_id).first():
            self.close()

        group_name = self.__class__.get_group_name(checkout_id)
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

        accept_subprotocol(self)
        logger.info(f"Checkout consumer {group_name} connected")

    def checkout_event(self, message):
        logger.info(f"Message received: {message}")
        message.pop("type", None)
        message["event"] = message.pop("event_name", None)

        logger.debug(f"Sending {message['event']} notification on {self.channel_name}...")
        self.send_json(message)
