-- sql/init.sql
-- Creates and populates the database used by the Irish noun parser.

DROP DATABASE IF EXISTS grammar_db;
CREATE DATABASE grammar_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE grammar_db;


-- Lexical Entries: Stores dictionary-level information for each lemma.
CREATE TABLE lexical_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lemma VARCHAR(255) NOT NULL,
    part_of_speech VARCHAR(50) NOT NULL,
    definition TEXT NOT NULL,
    CONSTRAINT uq_lexical_entry
        UNIQUE (lemma, part_of_speech)
);


-- Nouns: Stores noun-specific grammatical information, each noun belongs to one lexical entry.
CREATE TABLE nouns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lexical_entry_id INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    declension VARCHAR(50) NOT NULL,
    CONSTRAINT uq_noun_lexical_entry
        UNIQUE (lexical_entry_id),
    CONSTRAINT fk_noun_lexical_entry
        FOREIGN KEY (lexical_entry_id)
        REFERENCES lexical_entries(id)
        ON DELETE CASCADE
);


-- Noun Forms: Stores individual inflected forms of each noun.
CREATE TABLE noun_forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    noun_id INT NOT NULL,
    surface_form VARCHAR(255) NOT NULL,
    grammatical_case VARCHAR(50) NOT NULL,
    grammatical_number VARCHAR(50) NOT NULL,
    mutation VARCHAR(50) NOT NULL,
    CONSTRAINT fk_noun_form_noun
        FOREIGN KEY (noun_id)
        REFERENCES nouns(id)
        ON DELETE CASCADE
);



-- Representative Data: These manually entered paradigms provide stable data for repository, service, API, and end-to-end testing.

-- TEACH
INSERT INTO lexical_entries (
    lemma,
    part_of_speech,
    definition
)
VALUES (
    'teach',
    'noun',
    'house'
);
SET @teach_lexical_entry_id = LAST_INSERT_ID();
INSERT INTO nouns (
    lexical_entry_id,
    gender,
    declension
)
VALUES (
    @teach_lexical_entry_id,
    'masculine',
    'second'
);
SET @teach_noun_id = LAST_INSERT_ID();
INSERT INTO noun_forms (
    noun_id,
    surface_form,
    grammatical_case,
    grammatical_number,
    mutation
)
VALUES
    (@teach_noun_id, 'teach',    'nominative', 'singular', 'none'),
    (@teach_noun_id, 'tithe',    'nominative', 'plural',   'none'),

    (@teach_noun_id, 'a theach', 'vocative',   'singular', 'lenition'),
    (@teach_noun_id, 'a thithe', 'vocative',   'plural',   'lenition'),

    (@teach_noun_id, 'tí',       'genitive',    'singular', 'none'),
    (@teach_noun_id, 'tithe',    'genitive',    'plural',   'none'),

    (@teach_noun_id, 'teach',    'dative',      'singular', 'none'),
    (@teach_noun_id, 'tithe',    'dative',      'plural',   'none');

-- MADRA
INSERT INTO lexical_entries (
    lemma,
    part_of_speech,
    definition
)
VALUES (
    'madra',
    'noun',
    'dog'
);
SET @madra_lexical_entry_id = LAST_INSERT_ID();
INSERT INTO nouns (
    lexical_entry_id,
    gender,
    declension
)
VALUES (
    @madra_lexical_entry_id,
    'masculine',
    'fourth'
);
SET @madra_noun_id = LAST_INSERT_ID();
INSERT INTO noun_forms (
    noun_id,
    surface_form,
    grammatical_case,
    grammatical_number,
    mutation
)
VALUES
    (@madra_noun_id, 'madra',     'nominative', 'singular', 'none'),
    (@madra_noun_id, 'madraí',    'nominative', 'plural',   'none'),

    (@madra_noun_id, 'a mhadra',  'vocative',   'singular', 'lenition'),
    (@madra_noun_id, 'a mhadraí', 'vocative',   'plural',   'lenition'),

    (@madra_noun_id, 'madra',     'genitive',    'singular', 'none'),
    (@madra_noun_id, 'madraí',    'genitive',    'plural',   'none'),
    
    (@madra_noun_id, 'madra',     'dative',      'singular', 'none'),
    (@madra_noun_id, 'madraí',    'dative',      'plural',   'none');
