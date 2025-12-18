-- triggers for memories table

CREATE TRIGGER memories_after_update
AFTER UPDATE ON memories
FOR EACH ROW
BEGIN
	INSERT INTO hardware_updates (
		hardware_id,
		table_name,
		operation_type,
		old_data,
		new_data
	) VALUES (
		NEW.HARDWARE_ID,
		'memories',
		'UPDATE',
		JSON_OBJECT(
			'capacity', OLD.CAPACITY,
			'numslots', OLD.NUMSLOTS
		),
		JSON_OBJECT(
			'capacity', NEW.CAPACITY,
			'numslots', NEW.NUMSLOTS
		)
	);
END$$


CREATE TRIGGER memories_after_insert
AFTER INSERT ON memories
FOR EACH ROW
BEGIN
	INSERT INTO hardware_updates (
		hardware_id,
		table_name,
		operation_type,
		old_data,
		new_data
	) VALUES (
		NEW.HARDWARE_ID,
		'memories',
		'INSERT',
		NULL,
		JSON_OBJECT(
			'capacity', NEW.CAPACITY,
			'numslots', NEW.NUMSLOTS
			)
		);
END$$


CREATE TRIGGER memories_after_delete
AFTER DELETE ON memories
FOR EACH ROW 
BEGIN
	INSERT INTO hardware_updates (
		hardware_id,
		table_name,
		oepration_type,
		old_data,
		new_data
	) VALUES (
		OLD.HARDWARE_ID,
		'memories',
		'DELETE',
		JSON_OBJECT(
			'capacity', OLD.CAPACITY,
			'numslots', OLD.NUMSLOTS
		),
		NULL
	);
END$$

