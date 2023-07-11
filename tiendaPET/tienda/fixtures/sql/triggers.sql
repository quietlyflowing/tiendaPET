CREATE TRIGGER update_valor_total_after_insert AFTER INSERT ON tienda_detallecarrito
FOR EACH ROW
BEGIN
    UPDATE tienda_carrito
    SET valor_total = (
        SELECT SUM(precio_total)
        FROM tienda_detallecarrito
        WHERE carrito_id = NEW.carrito_id
    )
    WHERE id = NEW.carrito_id;
END;


CREATE TRIGGER update_cantidad_total_after_insert AFTER INSERT ON tienda_detallecarrito
FOR EACH ROW 
BEGIN 
	UPDATE tienda_carrito 
	SET cantidad_total = (
		SELECT SUM(cantidad)
		FROM tienda_detallecarrito 
		WHERE carrito_id = NEW.carrito_id
	)
	WHERE id = NEW.carrito_id;
END;

CREATE TRIGGER update_cantidad_total_after_update AFTER UPDATE ON tienda_detallecarrito
FOR EACH ROW 
BEGIN 
	UPDATE tienda_carrito 
	SET cantidad_total = (
		SELECT SUM(cantidad)
		FROM tienda_detallecarrito 
		WHERE carrito_id = NEW.carrito_id
	)
	WHERE id = NEW.carrito_id;
END;


CREATE TRIGGER update_valor_total_after_update AFTER UPDATE ON tienda_detallecarrito
FOR EACH ROW
BEGIN
    UPDATE tienda_carrito
    SET valor_total = (
        SELECT SUM(precio_total)
        FROM tienda_detallecarrito
        WHERE carrito_id = NEW.carrito_id
    )
    WHERE id = NEW.carrito_id;
END;

CREATE TRIGGER delete_carro_after_delete AFTER DELETE ON tienda_detallecarrito
FOR EACH ROW 
BEGIN 
	DELETE FROM tienda_carrito 
	WHERE id = OLD.carrito_id;
END;
