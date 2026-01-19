# OCS to Odoo Sync

**Status**: 🚧 Work in Progress

Python application that syncs hardware inventory data from OCS Inventory to Odoo's Asset Manager module via REST API.

## Overview

Monitors OCS Inventory database changes using MySQL triggers and automatically pushes computer hardware updates to Odoo in configurable batches. Designed to work with the custom Odoo Asset Manager endpoint.

## How It Works

1. **MySQL triggers** log changes to CPU, GPU, RAM, and monitors in `hardware_updates` table
2. **Python app** queries pending changes and aggregates hardware data
3. **Batch processing** sends updates to Odoo endpoint
4. **Auto-marking** processed changes to avoid duplicates

## Features

- Real-time change tracking via database triggers
- Batch processing with configurable size (default: 50)
- Multi-GPU detection and aggregation
- Memory stick counting and formatting (e.g., "2x8192MB + 1x4096MB")
- Monitor data collection and linking
- Dual logging (file + console)
- Marks processed changes to prevent duplicates

## Quick Start

### Prerequisites

- Python 3.7+
- MySQL/MariaDB access to OCS Inventory database
- Odoo instance with Asset Manager module installed
- Network access to Odoo API

### Installation

```bash
# Clone repository
git clone https://github.com/Andrei05231/ocs_to_odoo.git
cd ocs_to_odoo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install pymysql requests python-dotenv
```

### Database Setup

Install triggers to track hardware changes:

```bash
# Connect to OCS database
mysql -u your_user -p ocsweb

# Run setup scripts in order
mysql -u your_user -p ocsweb < ocs_db_changes/create_updates_table.sql
mysql -u your_user -p ocsweb < ocs_db_changes/hardware_triggers.sql
mysql -u your_user -p ocsweb < ocs_db_changes/memory_triggers.sql
mysql -u your_user -p ocsweb < ocs_db_changes/gpu_triggers.sql
mysql -u your_user -p ocsweb < ocs_db_changes/monitor_triggers.sql
```

### Configuration

Create `.env` file in project root:

```env
# OCS Database Configuration
OCS_DB_HOST=localhost
OCS_DB=ocsweb
OCS_USER=ocs_readonly_user
OCS_PASSWORD=your_secure_password

# Odoo API Configuration
ODOO_HOST=https://your-odoo-instance.com/web/dataset/call_kw/assets_computer/batch_update
ODOO_API_KEY=your_api_key_here
ODOO_DB=production_db
```

**Note**: Use a read-only MySQL user for OCS database access when possible.

### Running the Sync

```bash
# Activate virtual environment
source venv/bin/activate

# Run sync
python main.py
```

**Output**:
```
2025-01-19 10:30:15 - INFO - Starting OCS to Odoo transfer
2025-01-19 10:30:15 - INFO - Database connection successful
2025-01-19 10:30:15 - INFO - Got 15 pending changes
2025-01-19 10:30:15 - INFO - Found 8 computers with changes
2025-01-19 10:30:16 - INFO - Sending 8 computers to Odoo
2025-01-19 10:30:17 - INFO - Successfully sent computers to Odoo
2025-01-19 10:30:17 - INFO - Marked [1,2,3,4,5,6,7,8] as processed
2025-01-19 10:30:17 - INFO - Sync complete: 8 sent, 0 failed
```

## Data Flow

```
OCS Database Changes
        ↓
  MySQL Triggers
        ↓
hardware_updates table
        ↓
  Python App (queries pending)
        ↓
Aggregate Data (hardware, bios, videos, memories, monitors)
        ↓
  Format for Odoo
        ↓
  Batch Send via REST API
        ↓
  Mark as Processed
```

## Payload Format

Data sent to Odoo endpoint:

```json
{
  "context": {},
  "payload": {
    "computers": [
      {
        "name": "WORKSTATION-01",
        "serialNumber": "ABC123456789",
        "cpu": "Intel Core i7-9700K CPU @ 3.60GHz",
        "gpu": "NVIDIA GeForce RTX 2060, Intel UHD Graphics 630",
        "memory": "2x8192MB",
        "monitors": [
          {
            "name": "Dell U2720Q",
            "model": "Dell Monitor",
            "serial": "MON123456"
          }
        ]
      }
    ]
  }
}
```

## Database Triggers

### Tracked Changes

**Hardware Table** (`hardware_triggers.sql`):
- CPU changes (`PROCESSORT` field)
- IP adress changes (`IPADDR` field)

**Videos Table** (`gpu_triggers.sql`):
- GPU name changes
- GPU memory changes

**Memories Table** (`memory_triggers.sql`):
- RAM capacity changes
- Memory slot changes

**Monitors Table** (`monitor_triggers.sql`):
- Monitor name changes
- Serial number changes

### hardware_updates Table Schema

```sql
CREATE TABLE hardware_updates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hardware_id INT NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    operation_type ENUM('INSERT', 'UPDATE', 'DELETE'),
    old_data JSON,
    new_data JSON,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed TINYINT(1) DEFAULT 0,
    processed_at TIMESTAMP NULL,
    INDEX idx_processed (processed, changed_at),
    INDEX idx_hardware_id (hardware_id)
);
```

## Project Structure

```
ocs_to_odoo/
├── api/
│   ├── __init__.py
│   └── odoo_client.py         # Odoo REST API client
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration loading from .env
├── core/
│   ├── __init__.py
│   └── computer.py            # Computer data model and formatting
├── database/
│   ├── __init__.py
│   ├── connection.py          # MySQL connection handler
│   └── queries.py             # OCS database queries
├── ocs_db_changes/
│   ├── create_updates_table.sql
│   ├── hardware_triggers.sql
│   ├── memory_triggers.sql
│   ├── gpu_triggers.sql
│   └── monitor_triggers.sql
├── logs/                      # Auto-created log directory
├── .env                       # Configuration (not in git)
├── .gitignore
├── main.py                    # Application entry point
└── README.md
```

## Configuration Options

Edit `config/settings.py` to modify:

```python
app_config = AppConfig(
    batch_size=50,                    # Computers per batch
    log_file="logs/ocs_to_odoo.log",  # Log file path
    log_level="INFO"                  # DEBUG, INFO, WARNING, ERROR
)
```

## Data Processing

### Memory Aggregation

Converts individual memory stick records into summary format:

**OCS Data**:
```
Slot 1: 8192MB
Slot 2: 8192MB
Slot 3: 4096MB
```

**Output**: `"2x8192MB + 1x4096MB"`

### GPU Aggregation

Combines multiple GPU entries:

**OCS Data**:
```
GPU 1: NVIDIA GeForce RTX 2060
GPU 2: Intel UHD Graphics 630
```

**Output**: `"NVIDIA GeForce RTX 2060, Intel UHD Graphics 630"`

### Monitor Collection

Gathers all monitors for each computer:

```python
[
    {"name": "Dell U2720Q", "model": "Dell", "serial": "ABC123"},
    {"name": "HP E243", "model": "HP Monitor", "serial": "XYZ789"}
]
```

## Logging

Logs are written to both file and console:

**Log Location**: `logs/ocs_to_odoo.log`

**Log Format**:
```
2025-01-19 10:30:15 - module_name - INFO - Message text
```

**Log Levels**:
- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational messages
- **WARNING**: Non-critical issues (e.g., computers not found in Odoo)
- **ERROR**: Critical failures requiring attention

## Error Handling

- **Database Connection Failures**: Logs error and exits
- **Missing Hardware**: Skips computer, logs warning
- **API Errors**: Logs response, doesn't mark as processed (will retry next run)

## Scheduling

Run periodically using cron (Linux) or Task Scheduler (Windows):

### Linux Cron

```bash
# Edit crontab
crontab -e

# Run every 5 minutes
*/5 * * * * cd /path/to/ocs_to_odoo && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

### Windows Task Scheduler

Create task to run `main.py` with Python interpreter from virtual environment.

## Troubleshooting

### No Changes Detected

```bash
# Check if triggers are installed
mysql -u user -p ocsweb -e "SHOW TRIGGERS LIKE 'hardware'"

# Manually verify hardware_updates table
mysql -u user -p ocsweb -e "SELECT * FROM hardware_updates WHERE processed = 0"
```

### Connection Errors

```bash
# Test OCS database connection
mysql -u user -p -h hostname ocsweb -e "SELECT COUNT(*) FROM hardware"

# Test Odoo endpoint
curl -X POST https://your-odoo.com/endpoint -H "Content-Type: application/json"
```

### Computers Not Updated in Odoo

Check Odoo logs for endpoint errors. Common issues:
- Serial number mismatch
- Computer not found in Odoo
- Missing project/company assignment

## Limitations & Future Improvements

**Current Limitations**:
- Read-only sync (OCS → Odoo only)
- No storage/network adapter tracking
- Manual trigger installation required

**Planned Features**:
- [ ] Storage device tracking
- [ ] Network adapter information
- [ ] BIOS version tracking
- [ ] Automated trigger deployment
- [ ] Webhook support for instant updates
- [ ] Conflict resolution for simultaneous changes

## Security Notes

- Use read-only database user for OCS when possible
- Store `.env` file outside web-accessible directories
- Use HTTPS for Odoo API endpoint
- Rotate API keys regularly
- Review logs for suspicious activity

## Dependencies

```
pymysql>=1.0.0        # MySQL database connector
requests>=2.31.0      # HTTP client for Odoo API
python-dotenv>=1.0.0  # Environment variable management
```


## Version

**Current**: Work in Progress

