-- sql/init.sql
-- Creates and populates the database used by the Irish noun parser.

DROP DATABASE IF EXISTS grammar_db;
CREATE DATABASE grammar_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE grammar_db;


-- Lexical Entries: Stores dictionary-level information for each lemma.
-- part_of_speech:  1 = noun; 2 = verb; 3 = adjective
-- ==========================================================
CREATE TABLE lexical_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lemma VARCHAR(255) NOT NULL,
    part_of_speech TINYINT UNSIGNED NOT NULL,
    definition TEXT NOT NULL,

    CONSTRAINT uq_lexical_entry
        UNIQUE (lemma, part_of_speech),

    CONSTRAINT chk_part_of_speech
        CHECK (part_of_speech BETWEEN 1 AND 3)
);


-- Nouns: Stores noun-specific grammatical information.
-- gender: 1 = masculine; 2 = feminine
-- declension: 1 = first; 2 = second; 3 = third; 4 = fourth; 5 = fifth
-- ==========================================================
CREATE TABLE nouns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lexical_entry_id INT NOT NULL,
    gender TINYINT UNSIGNED NOT NULL,
    declension TINYINT UNSIGNED NOT NULL,

    CONSTRAINT uq_noun_lexical_entry
        UNIQUE (lexical_entry_id),

    CONSTRAINT chk_noun_gender
        CHECK (gender BETWEEN 1 AND 2),

    CONSTRAINT chk_noun_declension
        CHECK (declension BETWEEN 1 AND 5),

    CONSTRAINT fk_noun_lexical_entry
        FOREIGN KEY (lexical_entry_id)
        REFERENCES lexical_entries(id)
        ON DELETE CASCADE
);


-- Noun Forms: Stores individual inflected forms.
-- grammatical_case: 1 = nominative; 2 = genitive; 3 = dative; 4 = vocative
-- grammatical_number: 1 = singular; 2 = plural
-- mutation: 1 = none; 2 = lenition; 3 = eclipsis
-- ==========================================================
CREATE TABLE noun_forms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    noun_id INT NOT NULL,
    surface_form VARCHAR(255) NOT NULL,
    grammatical_case TINYINT UNSIGNED NOT NULL,
    grammatical_number TINYINT UNSIGNED NOT NULL,
    mutation TINYINT UNSIGNED NOT NULL,

    CONSTRAINT chk_noun_form_case
        CHECK (grammatical_case BETWEEN 1 AND 4),

    CONSTRAINT chk_noun_form_number
        CHECK (grammatical_number BETWEEN 1 AND 2),

    CONSTRAINT chk_noun_form_mutation
        CHECK (mutation BETWEEN 1 AND 3),

    CONSTRAINT fk_noun_form_noun
        FOREIGN KEY (noun_id)
        REFERENCES nouns(id)
        ON DELETE CASCADE
);


-- Representative Data: Provides stable data for repository, service, API, and end-to-end testing.

-- TEACH: noun = 1; masculine = 1; second declension = 2
-- ----------------------------------------------------------
INSERT INTO lexical_entries (
    lemma,
    part_of_speech,
    definition
)
VALUES (
    'teach',
    1,
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
    1,
    2
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
    -- Nominative
    (@teach_noun_id, 'teach',    1, 1, 1),
    (@teach_noun_id, 'tithe',    1, 2, 1),
    -- Genitive
    (@teach_noun_id, 'tí',       2, 1, 1),
    (@teach_noun_id, 'tithe',    2, 2, 1),
    -- Dative
    (@teach_noun_id, 'teach',    3, 1, 1),
    (@teach_noun_id, 'tithe',    3, 2, 1),
    -- Vocative
    (@teach_noun_id, 'a theach', 4, 1, 2),
    (@teach_noun_id, 'a thithe', 4, 2, 2);


-- MADRA: noun = 1; masculine = 1; fourth declension = 4
-- ------------------------------------------------------------
INSERT INTO lexical_entries (
    lemma,
    part_of_speech,
    definition
)
VALUES (
    'madra',
    1,
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
    1,
    4
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
    -- Nominative
    (@madra_noun_id, 'madra',     1, 1, 1),
    (@madra_noun_id, 'madraí',    1, 2, 1),
    -- Genitive
    (@madra_noun_id, 'madra',     2, 1, 1),
    (@madra_noun_id, 'madraí',    2, 2, 1),
    -- Dative
    (@madra_noun_id, 'madra',     3, 1, 1),
    (@madra_noun_id, 'madraí',    3, 2, 1),
    -- Vocative
    (@madra_noun_id, 'a mhadra',  4, 1, 2),
    (@madra_noun_id, 'a mhadraí', 4, 2, 2);
