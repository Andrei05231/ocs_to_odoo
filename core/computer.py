from dataclasses import dataclass
from typing import Optional
from collections import Counter

@dataclass
class Computer:
    name:str
    serial_number:str
    cpu:str
    gpu:str
    memory:str

    def format_for_odoo(self):
        return {
            'name':self.name,
            'serialNumber':self.serial_number,
            'cpu':self.cpu,
            'gpu':self.gpu,
            'memory':self.memory
        }

    @classmethod
    def process_ocs_data(cls, hardware_data, bios_data, vide_data, memory_data ):
        memory_str = ''
        if memory_data:
            stick_groups = Counter()

            for stick in memory_data:
                capacity = stick.get('capacity',0)
                if capacity > 0 :
                    stick_groups[capacity] +=1

            if stick_groups:
                parts = []
                for capacity, count in sorted(stick_groups.items(), reverse=True):
                    parts.append(f"{count}x{capacity}MB")

                memory_str = " + ".join(parts)

        return cls(
            name = hardware_data.get('name',''),
            serial_number = bios_data.get('serialNumber',''),
            cpu = hardware_data.get('cpu',''),
            gpu = video_data.get('gpu',''),
            memory = memory_str
            )
