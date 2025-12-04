# HobbyHub

## Overview
HobbyHub is a full-stack web app built with Django and styled with PicoCSS. 

HobbyHub is designed to help users track their hobbies and monitor their progress over time. Users can also connect with friends to see their hobby activity and follow their progress. They can share short messages of encouragement to help keep each other motivated.

This project was built as part of a full-stack web development course.

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

## Setup
### Run HobbyHub in Your Browser
HobbyHub is deployed on Fly.io.  
You can try the live version here: https://hobbyhub.fly.dev/

### Run HobbyHub Locally
1. Clone the repository  
     ` git clone https://github.com/lewis12307/HobbyHub.git`  
     `cd hobbyhub`

2. Create and activate a virtual environment:  
     `python3 -m venv venv`  
     `source venv/bin/activate     # macOS/Linux`   
     `venv\Scripts\activate        # Windows`  
3. Install dependencies:  
     `pip install -r requirements.txt`    
4. Apply database migrations:  
     `python manage.py migrate`  
5. Start the development server:  
     `python manage.py runserver`  
6. Visit the app at:  
     `http://127.0.0.1:8000/`

