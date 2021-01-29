DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS runs;
DROP TRIGGER IF EXISTS calculate_avg_speed_after_insert;
DROP TRIGGER IF EXISTS calculate_avg_speed_after_update;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  dist REAL NOT NULL,
  h INTEGER,
  m INTEGER,
  s INTEGER,
  speed REAL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TRIGGER calculate_avg_speed_after_insert
  AFTER INSERT ON runs
BEGIN
  UPDATE runs
  SET speed = new.dist/(CAST(new.h AS REAL) + CAST(new.m AS REAL)/60 + CAST(new.s AS REAL)/3600)
  WHERE id = new.id;
END;

CREATE TRIGGER calculate_avg_speed_after_update
  AFTER UPDATE ON runs
BEGIN
  UPDATE runs
  SET speed = new.dist/(CAST(new.h AS REAL) + CAST(new.m AS REAL)/60 + CAST(new.s AS REAL)/3600)
  WHERE id = new.id;
END;