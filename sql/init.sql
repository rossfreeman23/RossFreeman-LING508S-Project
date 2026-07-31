-- Recreate the database
DROP DATABASE IF EXISTS grammar_db;
CREATE DATABASE grammar_db;
USE grammar_db;

-- Lexical Entries: One dictionary entry (lemma) per row
CREATE TABLE lexical_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lemma VARCHAR(255) NOT NULL,
    part_of_speech VARCHAR(50) NOT NULL,
    definition TEXT NOT NULL
);

-- Nouns: Noun-specific grammatical properties
CREATE TABLE nouns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lexical_entry_id INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    declension VARCHAR(50) NOT NULL,
    FOREIGN KEY (lexical_entry_id)
        REFERENCES lexical_entries(id)
        ON DELETE CASCADE
);

-- Noun Forms: One row for every inflected form
CREATE TABLE noun_forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    noun_id INT NOT NULL,
    surface_form VARCHAR(255) NOT NULL,
    grammatical_case VARCHAR(50) NOT NULL,
    grammatical_number VARCHAR(50) NOT NULL,
    mutation VARCHAR(50) NOT NULL,
    FOREIGN KEY (noun_id)
        REFERENCES nouns(id)
        ON DELETE CASCADE
);

-- Samples present to develop and test against for repo, service layer, API
-- Should be replaced by scraper later on
-- Sample Lexical Entries
INSERT INTO lexical_entries
    (lemma, part_of_speech, definition)
VALUES
    ('teach', 'noun', 'house'),
    ('madra', 'noun', 'dog');

-- Sample Nouns
INSERT INTO nouns
    (lexical_entry_id, gender, declension)
VALUES
    (1, 'masculine', 'first'),
    (2, 'masculine', 'first');

-- Sample Noun Forms
INSERT INTO noun_forms
    (noun_id, surface_form, grammatical_case, grammatical_number, mutation)
VALUES
    -- teach
    (1, 'teach', 'nominative', 'singular', 'none'),
    (1, 'tithe', 'genitive', 'singular', 'none'),
    -- madra
    (2, 'madra', 'nominative', 'singular', 'none'),
    (2, 'madra', 'genitive', 'singular', 'lenition');
