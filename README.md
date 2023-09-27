# CSB Project I — Secure Mail

Link to the repository: https://github.com/joonas-a/SecureMail/tree/main

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

Virtual environment is used to avoid having possible issues with different Django versions.

Handle db migrations

- `python3 manage.py makemigrations`
- `python3 manage.py migrate`

Populate db with test users & messages

- `python3 manage.py setup_initial_data`

The app has no functionality for registering new users, so mock data users are needed in order to use the app.

Start the server

- `python3 manage.py runserver`

The app has the following users by default (username:password):

- alice : redqueen
- bob : sponge
- secure : mailer

## The flaws

### Flaw 1: Broken Access Control

https://github.com/joonas-a/SecureMail/blob/80ca7e0fc7ffcde252f57c8ab03e6dccb3849889/secure_mail/views.py#L40

- The application checks for login status, but only for home page. Currently users are able to view their messages (or any page besides the index) without logging in the app, by typing the url by hand.
  For example messages for user 'alice' can be seen by typing url `localhost:8000/messages/alice`.

- Fix: For fixing the vulnerability, django offers a solution with a decorator function @login_required. Uncommenting the decorator will cause Django to start checking whether a user is logged in or not before loading any messages. If user is not logged in the app will redirect user to the login screen. It is noteworthy that the function is part of django's own authentication system, and if not using it will probably not work.

### Flaw 2: SQL-Injection

https://github.com/joonas-a/SecureMail/blob/80ca7e0fc7ffcde252f57c8ab03e6dccb3849889/secure_mail/views.py#L92

- Action for sending new messages is using an insecure SQL-query, where user input is not sanitized at all, and which will execute every statement given to it even if all are part of the same string. If someone was to send a message to an existing user (alice, bob or secure) with content:

  `'); DROP TABLE secure_mail_message; --`

  the app would no longer function at all, unless the whole db was rebuilt. A perpetrator would also be able to, for example, steal user data from the database.

- Fix: Instead of using the very insecure executescript function (which will execute multiple scripts in one statement), we should use plain execute(), which will only execute a single SQL-statement. That doesn't fix the input not being sanitized though. A much better way with django would be to use django's built in ORM for database actions, which would take care of SQL-queries on it's own. The less SQL written manually, the less room for error.

### Flaw 3: Vulnerable and Outdated Components

https://github.com/joonas-a/SecureMail/blob/80ca7e0fc7ffcde252f57c8ab03e6dccb3849889/requirements.txt#L1

- The project is using Django version 4.1.6, which is prone to Denial of Service attacks by sending
  large Accept-Language HTML-headers.

- Fix: This has been fixed on later Django versions, and to fix the vulnerability in the project one would just have to change the Django version in `requirements.txt` to a newer one, such as v4.2.5, where said vulnerability doesn't exist. Hardcoding the specific dependency version may not be always best practice, and instead with requirements.txt we could use the following syntax for django: `Django>=4`, which would give us the latest Django 4 version. Upgrading from minor version to another shouldn't break the functionality, but to be safe we could also do `Django>=4.1`, which won't upgrade the minor version either, only the patch.

### Flaw 4: Identification and Authentication Failures

https://github.com/joonas-a/SecureMail/blob/80ca7e0fc7ffcde252f57c8ab03e6dccb3849889/secure_mail/views.py#L43

- Even if the login is now required, users are still able to view other user's messages, while logged in. This is due to the code not performing any checks, besides that the user is authenticated.

- Fix: There is a commented-out check, that makes sure that the currently logged in user's username matches the one who's messages we are trying to view.

### Flaw 5: CSRF-Vulnerability

https://github.com/joonas-a/SecureMail/blob/80ca7e0fc7ffcde252f57c8ab03e6dccb3849889/secure_mail/views.py#L77

- Django has taken care of CSRF-vulnerability by default. In order to have a vulnerability related to CSRF in the app, it's needed to explicitly declare a function not to be protected by using a decorative function @csrf_exempt.

- Fix: Uncomment the @csrf_exempt, and include a {% csrf_token %}-tag in the POST-form in messageForm.html.

### Minor flaw 6: Insecure Design

- The app isn't being tested in any way, besides the manual testing during development. The app expects the content length for new messages to be 200 characters at maximum (which is defined at the SQL-schema level), and has checks in the frontend for that. However message content length is not being tested in the backend, which shouldn't be the case, as one can easily bypass the frontend tests by sending the POST-data by some other mean, for example the Postman client. One doesn't need to be logged in in order to send new messages either, or even have an account in the system for that matter.

- Fix: Implement form input validation in the backend. Require new messages to be coming from an existing user. Setup E2E tests.
