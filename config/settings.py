import os 
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DBConfig():
    host:str
    db: str
    user:str
    password:str

@dataclass
class OdooConfig:
    host:str
    key:str
    db:str

@dataclass
class AppConfig:
    batch_size:int
    log_file:str
    log_level:str

def load_config():
    db_config = DBConfig(
        host=os.getenv('OCS_DB_HOST','localhost'),
        db=os.getenv('OCS_DB','ocsweb'),
        user=os.getenv('OCS_USER','user'),
        password=os.getenv('OCS_PASSWORD','password'),
    )

    odoo_config = OdooConfig(
        host = os.getenv('ODOO_HOST','localhsot'),
        key = os.getenv("ODOO_API_KEY",'api_key'),
        db = os.getenv('ODOO_DB','odoo_db'),
    )

    app_config = AppConfig(
        batch_size = 50,
        log_file = "logs/ocs_to_odoo.log",
        log_level = "INFO"
    )

    return db_config, odoo_config, app_config

