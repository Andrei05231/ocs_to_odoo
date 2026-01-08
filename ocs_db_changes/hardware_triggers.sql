-- triggers for hardware table

DELIMITER $$

DROP TRIGGER IF EXISTS hardware_after_update$$

CREATE TRIGGER hardware_after_update
AFTER UPDATE ON hardware
FOR EACH ROW
BEGIN
	IF NOT (
		OLD.PROCESSORT <=> NEW.PROCESSORT AND
		OLD.IPADDR <=> NEW.IPADDR
		) THEN
		INSERT INTO hardware_updates(
			hardware_id, 
			table_name,
			operation_type,
			old_data,
			new_data
		) VALUES (
			NEW.ID,
			'hardware',
			'UPDATE',
			JSON_OBJECT(
				'processor' , OLD.PROCESSORT,
				'ip', OLD.IPADDR
			),
			JSON_OBJECT(
				'processor', NEW.PROCESSORT,
				'ip', NEW.IPADDR
			)
		);

	END IF;
END$$


DROP TRIGGER IF EXISTS hardware_after_insert$$

CREATE TRIGGER hardware_after_insert
AFTER INSERT ON hardware
FOR EACH ROW
BEGIN
	INSERT INTO hardware_updates(
		hardware_id,
		table_name,
		operation_type,
		old_data,
		new_data
	) VALUES (
		ID,
		'hardware',
		'INSERT',
		NULL,
		JSON_OBJECT(
			'processor', NEW.PROCESSORT,
			'ip', NEW.IPADDR
		)
	);

END$$

DROP TRIGGER IF EXISTS hardware_after_delete$$

CREATE TRIGGER hardware_after_delete
AFTER DELETE ON hardware
FOR EACH ROW
BEGIN
	INSERT INTO hardware_updates(
		hardware_id,
		table_name,
		operation_type,
		old_data,
		new_data
	) VALUES (
		ID,
		'hardware',
		'DELETE',
		JSON_OBJECT(
			'processor', OLD.PROCESSORT,
			'ip', OLD.IPADDR
		),
		NULL
	);

END$$
