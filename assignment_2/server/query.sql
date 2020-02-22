CREATE TABLE players (
    sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ident VARCHAR(256),
    pass VARCHAR(256),
    x INTEGER,
    y INTEGER
);
CREATE TABLE planet (
    planet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(256) UNIQUE,
    width INTEGER,
    height, INTEGER
);
CREATE TABLE tiles (
    tile_id INTEGER PRIMARY KEY,
    x INTEGER,
    y INTEGER,
    elevation INTEGER,
    planet_id INTEGER,
    FOREIGN KEY (planet_id) REFERENCES planet(planet_id)
);
 CREATE TABLE player_tiles (
    player_id INTEGER,
    tile_id INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(sub_id),
    FOREIGN KEY (tile_id) REFERENCES tiles(tile_id),
    PRIMARY KEY (player_id, tile_id)
);
INSERT INTO players(ident, pass, x, y) VALUES ('admin', 'rebtrsgw', 0, 0);
INSERT INTO players(ident, pass, x, y) VALUES ('guest', 'qwzjoclp', 1, 0);
