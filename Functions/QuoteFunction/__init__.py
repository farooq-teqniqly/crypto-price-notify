import logging
import os
from ..shared import utilities as utils

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    settings = {
        'url': os.getenv('URL'),
        'currency': os.getenv('CURRENCY'),
        'shares': os.getenv('SHARES'),
        'notification_on_total': os.getenv('NOTIFICATION_ON_TOTAL')
    }

    soup = utils.make_soup(os.getenv('URL'))
    price = utils.get_price(soup, os.getenv('CURRENCY'))

    total = float(os.getenv('SHARES')) * float(price)
    notification_on_total = float(os.getenv('NOTIFICATION_ON_TOTAL'))

    message = 'Notification {0} sent. Total = {1}. Threshold = {2}.'

    if total > notification_on_total:
        logging.warning(message.format('', total, notification_on_total))
    else:
        logging.info(message.format('not', total, notification_on_total))
