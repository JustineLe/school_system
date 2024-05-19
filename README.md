# 🏫 School System

## 📑Problem Statement

The exercise is to create and update a few additional models and API endpoints.
This project is very similar to our backend tech stack.  

We use

- [Django 4](https://docs.djangoproject.com/en/4.0/)
- [django REST framework](https://www.django-rest-framework.org/)


Please complete all of the numbered tasks below.


### Models

1. Create a course model that represents a specific course/semester.

    - Properties:
        - `name`
        - `location` - example: `"Room 123"`

2. Create one or more models to represent school administrators, teachers and students.

    - Properties:
        - `name`

3. Create the following relationships between the previous models

    - A course can have 0-1 teachers
    - A course can have 0-many students
    - Each of the new models must be related to 1 school (use the `School` model provided)
    

### REST API

1. Create separate CRUD endpoints for the following

    - `courses`
    - `admins`
    - `teachers`
    - `students`

2. Add `GET /api/schools/:schoolId:/stats` which returns a JSON response with the following:

    ```
    {
        id: <schoolId>,
        courses: <# of courses>,
        admins: <# of admins>,
        teachers: <# of teachers>,
        students: <# of students>
    }
    ```

3. Create an endpoint `POST /api/transfer` that moves a student from one class to another.

    ```
    # Request body
    {
        studentId: <studentId>,
        fromCourseId: <current course ID>,
        toCourseId: <target course ID>
    }
    ```


## ✍️ Doing the exercise

This repository uses Docker and docker-compose to spin up two containers.  
One is a PostgreSQL database, and the other is a Python Django 4 application.

### Setup

1. To create the environment, run `docker-compose up -d` in the root directory of this repo.

    > M1 Mac users can run `docker-compose -f docker-compose.m1.yml up -d` instead.

2. Once the container is up and running, you will need to create a root user.  Run the following command and follow the prompts: 

    ```bash
    docker exec -it <container_name> poetry run python manage.py createsuperuser
    ```

3. You can view the Django admin at `http://localhost:8000/admin` using your new superuser credentials.

4. You can use [Postman](https://www.postman.com/) to test your endpoints.

### Test Driven Development

For speeding up the development we strongly recommend using [automated tests](https://realpython.com/test-driven-development-of-a-django-restful-api/) whenerever possible.
`django rest framework` provides [`APITestCase`](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases) 
to help developing APIs.
Making things testable will make them more modular.
Also, it makes the evaluation easier 😉.


## 💯 Evaluation

We will use the following process to verify your work.

1. Boot up the docker containers
2. Run/verify Django database migrations
3. Create some data using the Django admin tool
4. Evaluate the endpoints with your automated test scenarios (TDD)
5. Read your added documentation/diagrams/etc.

Your implementation will also be evaluated against the following criteria:

1. it has to work
2. cleanliness and readability of code
3. creativity --- it's great to show off interesting implementations, but stick to the objectives


> This exercise should not take too long, so don't feel the need to add extra features.
> Good luck!👍

For the Database Schema: View `school_database_schema.jpg`

To run test:
After start the docker container, run the command
> docker exec -it <container-name> poetry run python manage.py test

To view API docs: Please visit the endpoint
> {{host}}/redoc
