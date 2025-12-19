import requests
import logging
from config import OdooConfig
from core import Computer

logger = logging.getLogger(__name__)

class OdooClient:
    def __init__(self, config):
        self.config = config

    def send_batch(self, computers, change_ids):
        try:
            headers = {
                'Content-Type':'application/json',
                'X-Odoo-Database':self.config.db,
                }
            if self.config.key:
                headers['Authorization'] = f"Bearer {self.config.key}"

            payload = {
                    'context' : {},
                    'payload' : {
                    'computers': [ computer.format_for_odoo() for computer in computers ]
                    }
                }

            logger.info(f"Sending {len(computers)} computers to Odoo")

            response = requests.post(
                self.config.host,
                json = payload,
                headers = headers,
                timeout = 60
                    )

            if response.status_code in [200,201,202]:
                logger.info(f"Sucesfully sent computers to Odoo")
                return True
            else:
                logger.error(f"Could not send computers to Odoo: {e}")
                return False

        except Exception as e :
            logger.error(f"Error sending computer to Odoo: {e}")
            return False
