CREATE TABLE players
(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    status BOOL DEFAULT FALSE
)

CREATE TABLE solicitations
(
    id SERIAL PRIMARY KEY,
    value DECIMAL(15, 2) NOT NULL,
    player_id INTEGER,
    protocol INTEGER NOT NULL UNIQUE,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_player_id FOREIGN KEY (player_id) REFERENCES players (id) ON DELETE CASCADE
)

CREATE INDEX solicitations_index_protocol ON solicitations (protocol ASC)
