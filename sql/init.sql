DROP DATABASE IF EXISTS grammar_db;
CREATE DATABASE grammar_db;
USE grammar_db;
CREATE TABLE lexical_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    form VARCHAR(255),
    part_of_speech VARCHAR(50),
    definition TEXT,
    mutation VARCHAR(50)
);
INSERT INTO lexical_entries (form, part_of_speech, definition, mutation)
VALUES 
    ('teach', 'noun', 'house', 'none'),
    ('madra', 'noun', 'dog', 'lenition');
