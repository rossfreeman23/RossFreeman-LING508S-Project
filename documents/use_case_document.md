# USE CASE DOCUMENT

**Project:** Irish Morphological Parser (Single Nouns)

## Project Description

Inspired by the simplicity of the example in the Project Overview slides, I have decided that an application that would be a good one for me to learn on (i.e. be the first ever that I create) would be a noun parser in the language I am studying: Irish Gaelic.

## Use Case

### 1. Irish Noun Paradigm Lookup

*retrieve grammatical info & complete stored paradigm of single irish noun*

### Input

* a single noun / string in Irish Gaelic

**Examples:** teach, madra

### Output

all forms / info of the noun

* Lemma
* English definition
* Part of Speech
* Gender:

  * masculine or feminine
* Declension:

  * 1st
  * 2nd
  * 3rd
  * 4th
  * 5th
* All noun forms:

  * Surface form
  * Case:

    * nominative
    * vocative
    * genitive
    * dative
  * Number:

    * singular or plural
  * Mutation

    * ellipsis
    * lenition
    * none

### Access Methods

* HTML search form
* JSON API request

### Preconditions

* Flask application running
* MyQL database running & initialized
* Requested noun present in lexical database

### Main Success Scenario

1. User opens app’s HTML search page or sends JSON request to API
2. User enters one Irish noun lemma
3. Flask layer receives input
4. Flask layer passes noun to parser service
5. Parser service validates input
6. Parser service asks repo to find lemma
7. MySQL repo searches lexical database
8. Repo constructs corresponding LexicalEntry, Noun, and NounForm objects
9. Service converts domain objects into expected result
10. App displays noun paradigm as HTML page or returns it as JSON

### Alternative Scenarios

#### A. Empty Input

1. User submits empty value or only whitspace
2. App rejects input
3. App displays / returns error
4. Response uses HTTP status code 400

#### B. Invalid Input

1. API request does not contain JSON object or its word value is not a string
2. App rejects request
3. API returns explanatory error with HTTP status code 400

#### C. Noun Not Found

1. User submits noun not present in database
2. Repo returns no matching lexical entry
3. Service reports noun was not found
4. App displays / returns error with HTTP status code 404

### Postconditions

* Requested noun data displayed / returned when found
* Helpful error returned when input invalid or noun unavailable
* Lookup does not modify lexical database
