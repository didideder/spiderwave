CREATE TABLE genre( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE );

CREATE TABLE stream_url( id INTEGER PRIMARY KEY AUTOINCREMENT,
                         url TEXT UNIQUE,
                         bitrate INTEGER,
                         format TEXT );

CREATE TABLE country( id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE );

CREATE TABLE city( id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   country_id INTEGER,
                   FOREIGN KEY(country_id) REFERENCES country(id) );

CREATE TABLE radio( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    logo BLOB,
                    homepage TEXT,
                    city_id INTEGER,
                    valid INTEGER,
                    webonly INTEGER,
                    FOREIGN KEY(city_id) REFERENCES city(id) );

CREATE TABLE joingenre( id INTEGER PRIMARY KEY AUTOINCREMENT,
                        radio_id INTEGER,
                        genre_id INTEGER,
                        FOREIGN KEY(radio_id) REFERENCES radio(id),
                        FOREIGN KEY(genre_id) REFERENCES genre(id) );

CREATE TABLE joinurl( id INTEGER PRIMARY KEY AUTOINCREMENT,
                      radio_id INTEGER,
                      stream_url_id INTEGER,
                      FOREIGN KEY(radio_id) REFERENCES radio(id),
                      FOREIGN KEY(stream_url_id) REFERENCES stream_url(id) );
