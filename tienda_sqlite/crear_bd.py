import sqlite3
from pathlib import Path
DB = Path(__file__).resolve().parent / "tienda.db"
con = sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys = ON")
con.executescript("""
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY, nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL CHECK(precio >= 0),
    stock INTEGER NOT NULL CHECK(stock >= 0));
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY, nombre TEXT NOT NULL,
    ciudad TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INTEGER PRIMARY KEY,
    id_producto INTEGER NOT NULL REFERENCES productos(id_producto),
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente),
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    fecha TEXT NOT NULL);
""")
productos = [
    (1,'Laptop','Tecnología',750,12), (2,'Mouse','Tecnología',15,80),
    (3,'Teclado','Tecnología',30,45), (4,'Monitor','Tecnología',180,22),
    (5,'Escritorio','Muebles',220,14), (6,'Silla','Muebles',85,34),
    (7,'Impresora','Tecnología',250,10), (8,'Archivador','Muebles',120,18)]
clientes = [(1,'Ana Ruiz','Quito'),(2,'Luis Pérez','Guayaquil'),
    (3,'María Torres','Cuenca'),(4,'Carlos Díaz','Quito'),
    (5,'Sofía Vega','Ambato'),(6,'Pedro León','Loja')]
ventas = [
    (1,1,1,2,'2026-01-08'), (2,2,2,5,'2026-01-09'),
    (3,3,3,4,'2026-01-18'), (4,4,1,2,'2026-02-03'),
    (5,6,4,3,'2026-02-11'), (6,5,5,1,'2026-02-20'),
    (7,7,6,2,'2026-03-02'), (8,2,3,8,'2026-03-05'),
    (9,8,2,2,'2026-03-18'), (10,1,4,1,'2026-04-06'),
    (11,3,5,6,'2026-04-10'),(12,6,1,4,'2026-04-22'),
    (13,4,6,3,'2026-05-07'),(14,2,5,10,'2026-05-12'),
    (15,5,3,2,'2026-06-01')]
con.executemany('INSERT OR IGNORE INTO productos VALUES (?,?,?,?,?)', productos)
con.executemany('INSERT OR IGNORE INTO clientes VALUES (?,?,?)', clientes)
con.executemany('INSERT OR IGNORE INTO ventas VALUES (?,?,?,?,?)', ventas)
con.commit()
print('SQLite lista: tienda.db')
con.close()