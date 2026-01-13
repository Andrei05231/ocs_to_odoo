-- triggers for videos table

DELIMITER $$

DROP TRIGGER IF EXISTS videos_after_update $$

CREATE TRIGGER videos_after_update
AFTER UPDATE ON videos
FOR EACH ROW
BEGIN
	IF NOT (OLD.NAME<=>NEW.NAME) THEN
		INSERT INTO hardware_updates(
			hardware_id,
			table_name,
			operation_type,
			old_data,
			new_data
		) VALUES (
			NEW.HARDWARE_ID,
			'videos',
			'UPDATE',
			JSON_OBJECT(
				'name',OLD.NAME,
				'memory',OLD.MEMORY
			),
			JSON_OBJECT(
				'name', NEW.NAME,
				'memory', NEW.MEMORY
			)
		);

	END IF;
END$$


DROP TRIGGER IF EXISTS videos_after_insert$$

CREATE TRIGGER videos_after_insert
AFTER INSERT ON videos
FOR EACH ROW 
BEGIN
	INSERT INTO hardware_updates (
		hardware_id,
		table_name,
		operation_type,
		old_data,
		new_data
	) VALUES(
		NEW.HARDWARE_ID,
		'videos',
		'INSERT',
		NULL,
		JSON_OBJECT(
			'name',NEW.NAME,
			'memory',NEW.MEMORY
		)
	);

END$$



DROP TRIGGER IF EXISTS videos_after_delete$$

CREATE TRIGGER videos_after_delete
AFTER DELETE ON videos
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
		'videos',
		'DELETE',
		JSON_OBJECT(
			'name',OLD.NAME,
			'memory',OLD.MEMORY
		),
		NULL
	);
END$$

