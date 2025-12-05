# HobbyHub

## Overview
HobbyHub is a full-stack web app built with Django and styled with PicoCSS. 

HobbyHub is designed to help users track their hobbies and monitor their progress over time. Users can also connect with friends to see their hobby activity and follow their progress. Additionally, friends can share short messages of encouragement with one another to help keep each other motivated.

## Group Members
- Ari Osmun
- Lucy Lewis

## Features
### User Profiles
- Signup and Create a Profile
- Edit Your Profile
- Delete Your Profile
- Login / Logout

### Hobby Tracking
- Add a Hobby
- Delete a Hobby
- View Hobby details (time spent, number of sessions, associated sessions)
- View all Hobbies
- Sort Hobbies by Name, Start Date, Time Spent, Number of Sessions, or Recent Activity 
- Hobby Sessions to log progress for each Hobby
     - Add a Session (photo, text, or both)
     - Edit a Session
     - Delete a Session

### Friends System
- Look up other users by username
- Send friend requests
- Accept or Decline received friend requests
- View friends' profile and hobby activity

### Kudos 
- Send short supportive messages to friends
- View messages you’ve received, grouped into unseen (new) and viewed (old)

## Project Structure
HobbyHub is organized according to Django best practices. 

At the root level, we have the main `hobbyhub` project directory, which serves as the container for the entire application. It contains: 
- `manage.py`, which provides the command-line tools used to run the server, apply database migrations, and perform other project management tasks 
- `static/` folder, which stores the project’s static assets such as CSS, JavaScript, and design images
- `media/` folder, which stores all user-uploaded files such as profile pictures and hobby session images
- `templates/` folder, which stores project-wide HTML templates that are not tied to a specific Django app
- all Django apps (see below)
- the inner `hobbyhub/` project folder, which contains the core Django project files, including: 
     - `settings.py` which defines the project's global settings
     - `urls.py` which defines the root URL patterns for the entire project and links to the URL files of the other individual Django apps
     - `asgi.py` and `wsgi.py` which define how the overall application is configured and how it runs
- all configuration files
     - `requirements.txt`, which lists all dependencies needed to run the project 
     - `.dockerignore`, which specifies which files and folders should be excluded when building the Docker image for the project
     - `Dockerfile`, which defines how the Docker image for the application is built
     - `fly.toml`, which is the configuration file used by Fly.io to deploy and run the application


### Django Apps

Each major feature lives in its own Django app, with each app contained in its own folder. 
- `accounts/` contains all functionality related to user authentication (signup, login/logout) and profile management (viewing, editing, deleting profiles)
- `friends/` contains all functionality related to finding friends, sending friend requests, responding to friend requests, viewing friends, and removing friends
- `encouragement_notes/` contains all functionality related to sending kudos messages and viewing kudos messages received from friends
- `hobbies/` contains all functionality related to creating hobbies, deleting hobbies, viewing specific hobby details, viewing all your hobbies, and sorting hobbies
- `hobby_sessions/` contains all functionality related to creating, editing, and deleting hobby sessions associated with a specific hobby  

Each Django app folder includes:
- `apps.py`, which defines the app’s configuration so Django can register and manage the app
- `__init__.py`, which marks the folder as a Python package so the app and its modules can be imported correctly
- `urls.py`, which defines the feature’s URL patterns and maps them to the appropriate views
- `views.py`, which contains the logic for handling incoming HTTP requests related to the feature
- `models.py`, which defines the Django ORM models and database schema for the feature
- `migrations/` folder, which contains Django’s migration files that track and apply changes to the database schema
- `templates/<app name>` folder, which stores the HTML templates for the feature
- (Django app folders may also include a `forms.py` and `validators.py` when the feature requires custom forms or validation logic.)

## Setup
### Run HobbyHub in Your Browser
HobbyHub is deployed on Fly.io.  
You can try the live version here: https://hobbyhub.fly.dev/

### Run HobbyHub Locally
1. Clone the repository  
     ` git clone https://github.com/lewis12307/HobbyHub.git`  
2. Create and activate a virtual environment   
     `python3 -m venv venv`  
     `source venv/bin/activate     # macOS/Linux`   
     `venv\Scripts\activate        # Windows`  
3. Install dependencies  
     `pip install -r requirements.txt`    
4. Apply database migrations   
     `python manage.py migrate`  
5. Start the development server  
     `python manage.py runserver`  
6. Visit the app at:  
     `http://127.0.0.1:8000/`

