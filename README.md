# CSB Project I — Secure Mail

## A django messaging app with multiple vulnerabilities, and guidance on fixing them

### Prerequisites

- Have Python 3 installed

### Getting started

Commands are to be run in the root directory

Create python virtual environment

- `python3 -m venv venv`
- On linux/MacOS `source venv/bin/activate`
- Or on windows `venv\Scripts\activate`
- Install requirements with `pip install -r requirements.txt`

Handle db migrations

- `python3 manage.py makemigrations`
- `python3 manage.py migrate`

Populate db with test users & messages

- `python3 manage.py setup_initial_data`

Start the server

- `python3 manage.py runserver`

The app has the following users by default (username:password):

- alice:redqueen
- bob:sponge
- secure:mailer

## The flaws

### Flaw 1: Broken Access Control

- Be able to access own messages without logging in

### Flaw 2: SQL-Injection

- Creating a new message entry omits using Django ORM, and instead use plain SQL-queries.

### Flaw 3: Vulnerable and Outdated Components

- Use django@4.1.6

### Flaw 4: Identification and Authentication Failures

- Be able to view other users messages, when logged in as another user.

### Flaw 5: CSRF-Vulnerability

<!-- Documented in the code -->

- Sending new messages is @csrf_exempt
