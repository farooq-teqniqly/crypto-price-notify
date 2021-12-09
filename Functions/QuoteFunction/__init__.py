import json
import logging
import os
from ..shared import utilities as utils

import azure.functions as func


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

    notification.set(json.dumps({
        'currency': currency,
        'total': total,
        'threshold': notification_on_total,
        'delta': round(total - notification_on_total, 2)
    }))
