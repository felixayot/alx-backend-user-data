# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns a user based on the ID
- `DELETE /api/v1/users/:id`: deletes a user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates a user based on the ID (JSON parameters: `last_name` and `first_name`)
- `GET /api/v1/users/me`: retrieves the authenticated User object.
- `POST /api/v1/auth_session/login`: returns an authenticated user session.
- `DELETE /api/v1/auth_session/logout`: deletes an active user session. 
- `GET /api/v1/unauthorized`: returns an unauthorized request error code.
- `GET /api/v1/forbidden`: returns a forbidden request error code.
