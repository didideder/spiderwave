CREATE TABLE radio( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    logo BLOB,
                    homepage TEXT,
                    stream_url_ids TEXT,
                    genre_ids TEXT,
                    country_id INTEGER,
                    city_id INTEGER,
                    valid INTEGER,
                    webonly INTEGER );

CREATE TABLE city( id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   country_id INTEGER );
                   
CREATE TABLE country( id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE );
                      
CREATE TABLE genre( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE );

CREATE TABLE stream_url( id INTEGER PRIMARY KEY AUTOINCREMENT,
                         url TEXT UNIQUE,
                         bitrate INTEGER,
                         format TEXT );