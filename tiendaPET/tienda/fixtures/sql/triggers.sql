CREATE TRIGGER update_valorTotal_after_insert AFTER INSERT ON tienda_detallecarrito
FOR EACH ROW
BEGIN
    UPDATE tienda_carrito
    SET valorTotal = (
        SELECT SUM(precio_total)
        FROM tienda_detallecarrito
        WHERE carrito_id = NEW.carrito_id
    )
    WHERE id = NEW.carrito_id;
END;

CREATE TRIGGER update_valorTotal_after_update AFTER INSERT ON tienda_detallecarrito
FOR EACH ROW
BEGIN
    UPDATE tienda_carrito
    SET valorTotal = (
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
