import logging
from decimal import Decimal

from django.conf import settings
from django.test.signals import setting_changed

logger = logging.getLogger(__name__)


class AppSettings:
    class Transfer:
        minimum_confirmations = 10

    class Payment:
        minimum_confirmations = 5
        blockchain_route_lifetime = 100  # In blocks
        raiden_route_lifetime = 15 * 60  # In seconds

    class Raiden:
        minimum_ether_required = Decimal("0.025")
        minimum_service_token_required = Decimal("5.5")

    def __init__(self):
        self.load()

    def load(self):
        ATTRS = {
            "TRANSFER_MININUM_CONFIRMATIONS": (self.Transfer, "minimum_confirmations"),
            "PAYMENT_MININUM_CONFIRMATIONS": (self.Payment, "minimum_confirmations"),
            "PAYMENT_BLOCKCHAIN_ROUTE_LIFETIME": (self.Payment, "blockchain_route_lifetime"),
            "RAIDEN_MINIMUM_ETHER_REQUIRED": (self.Raiden, "minimum_ether_required"),
            "RAIDEN_MINIMUM_RDN_REQUIRED": (self.Raiden, "minimum_service_token_required"),
        }
        user_settings = getattr(settings, "HUB20", {})

        for setting, value in user_settings.items():
            if setting not in ATTRS:
                logger.warning(f"Ignoring {setting} as it is not a setting for HUB20")
                continue

            setting_class, attr = ATTRS[setting]
            setattr(setting_class, attr, value)


app_settings = AppSettings()


def reload_settings(*args, **kw):
    global app_settings
    setting = kw["setting"]
    if setting == "HUB20":
        app_settings.load()


setting_changed.connect(reload_settings)
