# Task manager

**This is the 4th training project of "Python Developer" course.**

Django web application for practicing CRUD operations and user permissions using ClassBasedViews, Models and TDD principles.

Deployed at: https://task-man.up.railway.app/

---
### Tests and code quality assessment:
[![Actions Status](https://github.com/Andrey-Volkovitskiy/python-django-developer-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Andrey-Volkovitskiy/python-django-developer-project-52/actions)    [![Linter](https://github.com/Andrey-Volkovitskiy/python-project-52/actions/workflows/flake8_linter.yml/badge.svg)](https://github.com/Andrey-Volkovitskiy/python-project-52/actions/workflows/flake8_linter.yml)    [![Pytest (with postgres)](https://github.com/Andrey-Volkovitskiy/python-project-52/actions/workflows/pytest_with_postgres.yml/badge.svg)](https://github.com/Andrey-Volkovitskiy/python-project-52/actions/workflows/pytest_with_postgres.yml)

[![Maintainability](https://api.codeclimate.com/v1/badges/b06b8d9b092a3a4c9712/maintainability)](https://codeclimate.com/github/Andrey-Volkovitskiy/python-project-52/maintainability)    [![Test Coverage](https://api.codeclimate.com/v1/badges/b06b8d9b092a3a4c9712/test_coverage)](https://codeclimate.com/github/Andrey-Volkovitskiy/python-project-52/test_coverage)


---
This project was built using these tools:

| Tool                                                                        | Description                                             |
|-----------------------------------------------------------------------------|---------------------------------------------------------|
| [Django](https://www.djangoproject.com/)         | Web framework  |
| [Django ORM](https://docs.djangoproject.com/en/4.2/topics/db/)         | Database-abstraction API  |
| [PostgreSQL](https://www.postgresql.org)         | Database management system  |
| [Bootstrap](https://getbootstrap.com/)         | CSS framework  |
| [Docker](https://www.docker.com)       | Container-based platform for building apps  |
| [Poetry](https://poetry.eustace.io/)         | Python dependency manager  |
| [Pytest](https://docs.pytest.org/)               | Testing framework |
| [Flake8](https://flake8.pycqa.org/)               | Linter to check code style |
| [Code Climate](https://codeclimate.com/)               | Clean Code verification system |
| [GitHub Actions](https://github.com/features/actions)               | Continuous Integration (CI) |
| [Railway](https://railway.app)               | Deployment platform |
| [Rollbar](https://rollbar.com/)               | Error logging & tracking service |


---
### Installation and running
The application stores data using PostgresSQL (connected via DATABASE_URL).

- *make install* - to install dependencies
- *make migrate* - to migrate a database
- *make start* - to start the application
- *make dev* - to start app on development web server
- *make test* - to run tests
- *make lint* - to run linter (Flake8h)

(more service commands can be found in Makefile)

---
![er diagram](https://github.com/Andrey-Volkovitskiy/python-project-52/blob/main/er_diagram.jpg?raw=true)
