# OCS to Odoo Sync

**Status**: 🚧 Work in Progress

A Python application that synchronizes hardware inventory data from OCS Inventory to Odoo through a custom endpoint.

## Overview

Monitors OCS Inventory database changes via MySQL triggers and automatically pushes computer hardware updates to a custom Odoo endpoint in batches.

## Features

- Change tracking via MySQL triggers (hardware, BIOS, video, memory)
- Batch processing with configurable size
- Automatic marking of processed changes
- File and console logging
- Data aggregation (multi-GPU, memory sticks)

## Quick Start

### Prerequisites

- Python 3.7+
- MySQL/MariaDB access to OCS Inventory
- Odoo instance with custom endpoint

### Installation

```bash
# Clone and setup
git clone https://github.com/Andrei05231/ocs_to_odoo.git
cd ocs_to_odoo
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pymysql requests python-dotenv

# Setup database triggers
mysql -u user -p ocsweb < ocs_db_changes/create_updates_table.sql
mysql -u user -p ocsweb < ocs_db_changes/memory_triggers.sql
mysql -u user -p ocsweb < ocs_db_changes/gpu_triggers.sql
```

### Configuration

Create `.env` file:

```env
OCS_DB_HOST=localhost
OCS_DB=ocsweb
OCS_USER=your_user
OCS_PASSWORD=your_password

ODOO_HOST=https://your-odoo-instance.com/api/endpoint
ODOO_API_KEY=your_api_key
ODOO_DB=your_odoo_database
```

### Run

```bash
python main.py
```

## Data Flow

1. OCS database triggers log changes to `hardware_updates` table
2. Application queries pending changes
3. Hardware info aggregated from multiple tables (hardware, bios, videos, memories)
4. Data formatted and sent to Odoo in batches
5. Processed changes marked as complete

## Payload Format

```json
{
  "context": {},
  "payload": {
    "computers": [
      {
        "name": "COMPUTER-01",
        "serialNumber": "ABC123456",
        "cpu": "Intel Core i7-9700K",
        "gpu": "NVIDIA GeForce RTX 2060",
        "memory": "2x8192MB"
      }
    ]
  }
}
```

## Project Structure

```
ocs_to_odoo/
├── api/              # Odoo API client
├── config/           # Configuration management
├── core/             # Computer data model
├── database/         # OCS database queries
├── ocs_db_changes/   # SQL triggers and schema
└── main.py           # Entry point
```

## Next

- [ ] Additional hardware fields (storage, network adapters)

