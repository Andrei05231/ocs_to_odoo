import logging 
from typing import List, Dict, Any, Optional
from .connection import DatabaseConnection
from core import Computer

logger = logging.getLogger(__name__)

class OCSQueries:
    def __init__(self, db_connection:DatabaseConnection):
        self.db = db_connection

    def get_pending_changes(self):
        try:
            with self.db.cursor() as cursor:
                query = """
                    SELECT
                        id,
                        hardware_id,
                        table_name,
                        operation_type,
                        old_data,
                        new_data,
                        chaged_at
                    FROM hardware_updates
                    WHERE processed = 0
                    ORDER BY changed_at ASC
                """
                cursor.execute(query)
                changes = cursor.fetchall()
                logger.info( f"Got {len(changes)} pending changes" )
                return changes
        except Exception as e:
            logger.error(f"Failed to fetch changes: {e}")
            return []

    def get_hardware_info(self, hardware_id):
        with self.db.cursor() as cursor:
            query = """ 
                SELECT NAME as name,
                PROCESSORT as cpu,
                MEMORY as memory
                FROM hardware
                WHERE ID = %s
            """
            cursor.execute(query, hardware_id)
            info = cursor.fetchone()
            return info

    def get_bios_info(self, hardware_id):
        with self.db.cursor() as cursor:
            query = """ 
                SELECT SSN as serialNumber
                FROM bios 
                WHERE HARDWARE_ID = %s
            """
            cursor.execute(query, hardware_id)
            return cursor.fetchone()


    def get_video_info(self, hardware_id):
        with self.db.cursor() as cursor:
            query = """ 
                SELECT NAME as gpu
                FROM videos 
                WHERE HARDWARE_ID = %s
            """  
            cursor.execute(query, hardware_id)
            return cursor.fetchall()

    def get_memory_info(self, harware_id):
        with self.db.cursor() as cursor:
            query = """ 
                SELECT CAPACITY as capacity,
                NUMSLOTS as slot_number
                FROM memories
                WHERE HARDWARE_ID = %s 
                AND CAPACITY > 0
                ORDER BY NUMSLOTS ASC
            """
            cursor.execute(query, hardware_id)
            return cursor.fetchall()

    def get_computer_info(self, hardware_id):
        try:
            hardware = self.get_hardware_info(hardware_id)
            if not hardware:
                logger.warning(f"Hardware {hardware_id} not found")
                return None
            bios = self.get_bios_info(hardware_id)
            video = self.get_video_info(hardware_id)
            memory = self.get_memory_info(hardware_id)

            return Computer.process_ocs_data(hardware, bios,video,memory)
        
        except Exception as e :
            logger.error(f"Could not get computer info for : {hardware_id}")
            return None


    def mark_as_processed(self,change_ids):
        try:
            with self.sb.cursor() as cursor:
                query = """ 
                    UPDATE hardware_update
                    SET processed = 1, processed_at = NOW()
                    WHERE ID IN (%s)
                """ % ','.join( ['%s'] * len(change_ids) ) 

                # .join stuff makes %s a comma separated value 

                cursor.execute(query, change_ids)
                logger.info(f"Marked {change_ids} as processed")
                return True
        except Exception as e:
            logger.error(f"Could not mark changes are processed:{e}")
            return False






