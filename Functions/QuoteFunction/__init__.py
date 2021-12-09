import json
import logging
import os

import azure.functions as func

from ..shared import utilities as utils


def main(mytimer: func.TimerRequest, notification: func.Out[str]) -> None:
    currency = os.getenv('CURRENCY')
    soup = utils.make_soup(os.getenv('URL'))
    price = utils.get_price(soup, currency)

    total = float(os.getenv('SHARES')) * float(price)
    notification_on_total = float(os.getenv('NOTIFICATION_ON_TOTAL'))

    message = 'Notification {0} sent. Total = {1}. Threshold = {2}.'

    if total <= notification_on_total:
        logging.info(message.format('not', total, notification_on_total))
        return

    logging.warning(message.format('', total, notification_on_total))

    notification_message = f"DELTA ALERT: {total - notification_on_total}"

    notification.set(notification_message)
