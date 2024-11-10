pub const CREATE_TABLE_USERS: &'static str = "
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        age INTEGER NOT NULL,
        avatar VARCHAR(256),
        gender VARCHAR(6),
        about TEXT
    );
";

pub const CREATE_TABLE_RIDES: &'static str = "
    CREATE TABLE IF NOT EXISTS rides (
        id INTEGER NOT NULL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        start_point_lat REAL NOT NULL,
        start_point_lng REAL NOT NULL,
        end_point_lat REAL NOT NULL,
        end_point_lng REAL NOT NULL
        start_period INTEGER NOT NULL,
        end_period INTEGER NOT NULL
    );
";

pub const CREATE_TABLE_CONFLICTS: &'static str = "
    CREATE TABLE IF NOT EXISTS conflicts (
        issuer_id INTEGER NOT NULL,
        target_id INTEGER NOT NULL
    );
";
