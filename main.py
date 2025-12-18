import logging
import os
from pathlib import Path

from config import load_config
from database import DatabaseConnection, OCSQueries
from api import OdooClient

def setup_logging(log_file, log_level):
    log_dir = Path(log_file).parent
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level = getattr(logging, log_level),
        format='%(asctime)s - $(name)s - %(levelname)s - %(message)s',
        handlers = [
            logging.FileHandler(log_file),
            logging.StreamHandler()
            ]
        )

def main():
    db_config, odoo_config, app_config = load_config()

    setup_logging(app_config.log_file, app_config.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting OCS to Odoo transfer")

    db_connection = DatabaseConnection(db_config)
    ocs_queries = OCSQueries(db_connection)
    odoo_client = OdooClient(odoo_config)

    try: 
        db_connection.connect()

        changes = ocs_queries.get_pending_changes()

        if not changes:
            logger.info("No pending Changes")
            return 

        hardware_ids = list( set( change['hardware_id'] for change in changes ) )
        logger.info(f"Found {len(hardware_ids)} computers with changes")

        total_sucessful = 0
        total_failed = 0 
        batch_size = app_config.batch_size

        for i in range( 0, len(hardware_ids) , batch_size ):
            batch_hw_ids = hardware_ids[i:i + batch_size]
            computers = []
            batch_changes_ids = []

            for hw_id in batch_hw_ids:
                computer  = ocs_queries.get_computer_info(hw_id)
                if computer:
                    computers.append(computer)

                    hw_changes_ids = [change['id'] for change in changes if change['hardware_id'] == hw_id]
                    batch_changes_ids.extend(hw_changes_ids)

            if computers:
                if odoo.client.send_batch(computers, batch_changes_ids):
                    if ocs_queries.mark_as_processed(batch_changes_ids):
                        total_sucessful += len(computers)
                    else:
                        total_failed +=len(computers)
                else:
                    total_failed+=len(computers)


        logger.info(f"Sync complete: {total_sucessful} sent, {total_failed} failed")

    except Exception as e:
        logger.error(f"Error in the main send function: {e}")
    finally:
        db_connection.close()

if __name__ == "__main__":
    main()

