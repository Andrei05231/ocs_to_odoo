-- triggers for monitors table 

DELIMITER $$

DROP TRIGGER IF EXISTS monitors_after_update &&

CREATE TRIGGER monitors_after_update
AFTER UPDATE ON monitors 
FOR EACH ROW 
BEGIN 
	IF NOT ( OLD.CAPTION <=> NEW.CAPTION) AND
	NOT (OLD.SERIAL <=> NEW.SERIAL) THEN
		INSERT INTO hardware_updates(
			hardware_id,
			table_name,
			operation_type,
			old_data,
			new_data
		) VALUES (
			NEW.HARDWARE_ID,
			'monitors',
			'UPDATE',
			JSON_OBJECT(
				'name', OLD.CAPTION,
				'serial', OLD.SERIAL
			),
			JSON_OBJECT(
				'name', NEW.CAPTION,
				'serial',NEW.SERIAL
			)

		);
	END IF;
END$$


DROP TRIGGER IF EXISTS monitors_after_instert&&
AFTER INSERT ON monitors
FOR EACH ROW 
BEGIN
	INSERT INTO hardware_updates(
		hardware_id,
		table_name,
		operation_type,
		old_data,
		new_data

	) VALUES (
		NEW.HARDWARE_ID,
		'monitors'.
		'INSERT',
		NULL,
		JSON_OBJECT(
			'name',NEW.CAPTION,
			'serial',NEW.SERIAL
		)
	);
END&&


DROP TRIGGER IF EXISTS monitors_after_delete
AFTER DELETE ON monitors
FOR EACH ROW 
BEGIN
	INSERT INTO hardware_updates(
		hardware_id,
		table_name,
		operation_type,
		old_data,
		new_data
	) VALUES (
		OLD.HARDWARE_ID,
		'monitors',
		'DELETE',
		JSON_OBJECT(
			'name',OLD.CAPTION,
			'serial',OLD.SERIAL
		),
		NULL
	);

END$$
