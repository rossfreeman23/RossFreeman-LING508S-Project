# Irish Noun Morphological Parser: API and UI Documentation

## Overview

The Irish Noun Morphological Parser retrieves grammatical information and the complete stored paradigm of a single Irish noun.

The application supports one primary use case:

> Given a single Irish noun lemma, retrieve its definition, part of speech, gender, declension, and all stored forms.

The use case can be accessed through:

1. An HTML search form
2. A JSON API request

## Base URL

When the Flask development server is running locally, the application is available at:

```text
http://127.0.0.1:5000
```

## Application Flow

```text
HTML form or JSON request
→ Flask application
→ parser service
→ repository interface
→ MySQL repository
→ grammar_db
→ domain objects
→ HTML or JSON response
```

The Flask layer does not query MySQL directly. It sends valid noun input to the separate parser service, which uses the repository layer to retrieve the requested lexical entry.

## Endpoint Summary

| Method | Endpoint  | Input                         | Output                                          |
| ------ | --------- | ----------------------------- | ----------------------------------------------- |
| `GET`  | `/`       | None                          | HTML noun search form                           |
| `POST` | `/search` | HTML form field named `word`  | HTML page containing the noun paradigm or error |
| `POST` | `/parse`  | JSON object containing `word` | JSON noun paradigm or error                     |

---

# HTML Form Interface

## Display the Search Form

### Request

```http
GET /
```

### Input

No input is required.

### Successful Response

```text
200 OK
Content-Type: text/html
```

The response displays the Irish noun search form.

The form contains:

* A text input named `word`
* A Search button
* An area for successful noun results
* An area for error messages

## Submit an HTML Search

### Request

```http
POST /search
Content-Type: application/x-www-form-urlencoded
```

### Input

| Field  | Type   | Required | Description               |
| ------ | ------ | -------: | ------------------------- |
| `word` | String |      Yes | A single Irish noun lemma |

Example form input:

```text
teach
```

### Successful Response

```text
200 OK
Content-Type: text/html
```

The rendered HTML page displays:

* Lemma
* English definition
* Part of speech
* Gender
* Declension
* Surface form
* Grammatical case
* Grammatical number
* Mutation

For `teach`, the page displays the definition `house`, masculine gender, second declension, and eight stored noun forms.

### Empty Input

If the form contains an empty string or only whitespace:

```text
400 BAD REQUEST
Content-Type: text/html
```

The page displays:

```text
word cannot be empty.
```

### Noun Not Found

If the noun is not present in the database:

```text
404 NOT FOUND
Content-Type: text/html
```

Example displayed error:

```text
Noun 'xyz' not found in database.
```

---

# JSON API

## Retrieve a Noun Paradigm

### Request

```http
POST /parse
Content-Type: application/json
```

### Expected Input

The request body must be a JSON object containing a `word` field.

```json
{
  "word": "teach"
}
```

The `word` value must:

* Be a string
* Contain a single Irish noun lemma
* Not be empty or whitespace
* Match a noun stored in the lexical database

Input matching is case-insensitive, and surrounding whitespace is removed before the database lookup.

## Example Request with `curl`

```bash
curl -i \
  -X POST \
  http://127.0.0.1:5000/parse \
  -H "Content-Type: application/json" \
  -d '{"word": "teach"}'
```

## Successful Response

```text
200 OK
Content-Type: application/json
```

Example response:

```json
{
  "declension": "second",
  "definition": "house",
  "forms": [
    {
      "case": "nominative",
      "mutation": "none",
      "number": "singular",
      "surface_form": "teach"
    },
    {
      "case": "nominative",
      "mutation": "none",
      "number": "plural",
      "surface_form": "tithe"
    },
    {
      "case": "genitive",
      "mutation": "none",
      "number": "singular",
      "surface_form": "tí"
    },
    {
      "case": "genitive",
      "mutation": "none",
      "number": "plural",
      "surface_form": "tithe"
    },
    {
      "case": "dative",
      "mutation": "none",
      "number": "singular",
      "surface_form": "teach"
    },
    {
      "case": "dative",
      "mutation": "none",
      "number": "plural",
      "surface_form": "tithe"
    },
    {
      "case": "vocative",
      "mutation": "lenition",
      "number": "singular",
      "surface_form": "a theach"
    },
    {
      "case": "vocative",
      "mutation": "lenition",
      "number": "plural",
      "surface_form": "a thithe"
    }
  ],
  "gender": "masculine",
  "lemma": "teach",
  "part_of_speech": "noun"
}
```

## Successful Output Fields

| Field                  | Type   | Description                               |
| ---------------------- | ------ | ----------------------------------------- |
| `lemma`                | String | Dictionary headword                       |
| `definition`           | String | English definition                        |
| `part_of_speech`       | String | Part of speech                            |
| `gender`               | String | Masculine or feminine                     |
| `declension`           | String | First through fifth declension            |
| `forms`                | Array  | Stored noun forms                         |
| `forms[].surface_form` | String | Inflected surface form                    |
| `forms[].case`         | String | Nominative, genitive, dative, or vocative |
| `forms[].number`       | String | Singular or plural                        |
| `forms[].mutation`     | String | None, lenition, or eclipsis               |

---

# API Error Responses

## Missing or Invalid JSON Body

A request without a JSON object returns:

```text
400 BAD REQUEST
```

```json
{
  "error": "Request body must be a JSON object."
}
```

Example:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:5000/parse
```

## Missing `word` Field

A JSON object without `word` returns:

```text
400 BAD REQUEST
```

```json
{
  "error": "word must be a string."
}
```

Example:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:5000/parse \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Non-String `word`

A `word` value that is not a string returns:

```text
400 BAD REQUEST
```

```json
{
  "error": "word must be a string."
}
```

Example:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:5000/parse \
  -H "Content-Type: application/json" \
  -d '{"word": 123}'
```

## Empty Input

An empty string or whitespace returns:

```text
400 BAD REQUEST
```

```json
{
  "error": "word cannot be empty."
}
```

Example:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:5000/parse \
  -H "Content-Type: application/json" \
  -d '{"word": ""}'
```

## Noun Not Found

A valid string that is not present in the database returns:

```text
404 NOT FOUND
```

```json
{
  "error": "Noun 'xyz' not found in database."
}
```

Example:

```bash
curl -i \
  -X POST \
  http://127.0.0.1:5000/parse \
  -H "Content-Type: application/json" \
  -d '{"word": "xyz"}'
```

---

# Running the Application

The complete installation and database setup instructions are available in the repository’s root-level `README.md`.

After installing the requirements, initializing `grammar_db`, and setting the MySQL environment variables, start Flask from the project root:

```bash
python3 app.py
```

Open the HTML interface at:

```text
http://127.0.0.1:5000
```

The JSON API is available at:

```text
http://127.0.0.1:5000/parse
```

---

# Testing

The Flask application has both isolated API tests and real end-to-end tests.

Run the isolated Flask tests:

```bash
python3 -m pytest tests/test_app.py -v
```

Run the real end-to-end tests after configuring MySQL:

```bash
python3 -m pytest tests/test_end_to_end.py -v
```

Run the complete suite:

```bash
python3 -m pytest -v
```

Final verified result:

```text
62 passed
```

The end-to-end tests verify both access methods:

* JSON API request through `POST /parse`
* HTML form submission through `POST /search`
