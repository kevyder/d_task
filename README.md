# Tasks API

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/1af62d73e5a14c7193b37b0f60485666)](https://www.codacy.com/gh/kevyder/d_task/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kevyder/d_task&amp;utm_campaign=Badge_Grade)[![Build Status](https://travis-ci.org/kevyder/d_task.svg?branch=master)](https://travis-ci.org/kevyder/d_task) [![Coverage Status](https://coveralls.io/repos/github/kevyder/d_task/badge.svg?branch=master)](https://coveralls.io/github/kevyder/d_task?branch=master)

System details:

* Python 3.8.2

* Django 3.1.1

* Django REST framework 3.12.1

## Usage

Install dependencies

```bash
pip3 install -r requirements.txt
```

Run server

```bash
python3 manape.py runserver
```

Run Tests

```bash
coverage run --source='.' manage.py test
```

Get tests coverage

```bash
coverage report
```

## Headers and Authentication

  > Content-Type: application/json
  > Authorization: Token=[token]

## Endpoints

> (*) for authentication required

### Sign Up - POST

> {HOST}/api/user/create/

* ### PARAMS.

  * name: string
  * email: string
  * password: string

### Get token - POST

> {HOST}/api/user/token/

#### params.

* email: string
* password: string

#### Create task (*) - POST

> {HOST}/api/task/

#### params.

* title: string
* description: string

#### Update task (*) - PUT

> {HOST}/api/task/:id

#### params.

* title: string
* description: string
* completed: boolean

#### List tasks (*) - GET

> {HOST}/api/task/

#### Get task (*) - GET

> {HOST}/api/task/:id

#### Delete task (*) - DELETE

> {HOST}/api/task/:id
