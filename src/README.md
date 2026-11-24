# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teacher login to manage activity registrations
- Students can view participants but cannot change registrations

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Configure a teacher username and password in the environment. Do not commit credentials:

   ```
   export TEACHER_USERNAME=teacher
   export TEACHER_PASSWORD='choose-a-strong-password'
   ```

   When serving the app over HTTPS, also set `COOKIE_SECURE=true`.

3. From the repository root, run the application:

   ```
   uvicorn src.app:app --reload
   ```

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

To run the authentication tests, install the test dependencies and run:

```
pip install -r requirements-test.txt
python -m unittest discover -s tests -v
```

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/status`                                                    | Check whether the current browser is logged in as a teacher         |
| POST   | `/auth/login`                                                     | Log in with the configured teacher username and password            |
| POST   | `/auth/logout`                                                    | Log out the current browser                                          |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up a student (teacher login required)                           |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher login required)                   |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All activities and teacher sessions are stored in memory, which means they reset when the server restarts. Teacher credentials are read from environment variables and must not be stored in source control.
