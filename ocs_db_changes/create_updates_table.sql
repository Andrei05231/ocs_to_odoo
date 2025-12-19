-- Create hardware_updates table for tracking changes

CREATE TABLE IF NOT EXISTS hardware_updates(
	id INT AUTO_INCREMENT PRIMARY KEY,
	hardware_id INT NOT NULL,
	table_name VARCHAR(100) NOT NULL,
	operation_type ENUM( 'INSERT', 'UPDATE', 'DELETE' ) NOT NULL,
	old_data JSON,
	new_data JSON,
	changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	processed TINYINT(1) DEFAULT 0,
	processed_at TIMESTAMP NULL,
	INDEX idx_processed ( processed, changed_at ),
	INDEX idx_hardware_id ( hardware_id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

