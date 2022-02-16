import sqlite3

conn = sqlite3.connect('cleopatra.sqlite')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS collections (
    id integer PRIMARY KEY AUTOINCREMENT UNIQUE,
    name text UNIQUE,
    rztk_name text,
    price text,
    pile_height text,
    material text,
    type text,
    apply text,
    design text,
    features text,
    description text, 
    description_ua text
);""")

cur.execute("""
CREATE TABLE IF NOT EXISTS models (
    id  integer PRIMARY KEY AUTOINCREMENT UNIQUE,
    name text,
    coll_id integer,
    form text,
    colours text,
    img text,        
    FOREIGN KEY (coll_id) REFERENCES collections (id)
);""")

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id  integer PRIMARY KEY AUTOINCREMENT UNIQUE,
    prod_id integer,
    model_id integer,
    size text,
    qty text,
    FOREIGN KEY (model_id) REFERENCES models (id)
);
""")

conn.commit()
cur.close()