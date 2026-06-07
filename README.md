# Social Book

A simple Django social media-style web application with user authentication, profile management, post creation, likes, and follow/unfollow interactions.

## Features

- User signup and sign-in
- Home feed with posts
- Upload new posts with captions and images
- Like and unlike posts
- User profiles and follow/unfollow actions
- Profile settings page

## Project Structure

- `social_book/` - Django project configuration
- `social_book/core/` - Main application logic, models, views, URLs, and templates
- `social_book/media/` - Uploaded images

## Requirements

- Python 3.11
- Django
- Pillow

## Setup

1. Install dependencies with Pipenv:

   ```bash
   pipenv install
   ```

2. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

3. Apply database migrations:

   ```bash
   cd social_book
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

5. Open the app in your browser:

   ```text
   http://127.0.0.1:8000/
   ```

## Useful Commands

- Create a superuser:

  ```bash
  python manage.py createsuperuser
  ```

- Run tests:

  ```bash
  python manage.py test
  ```

## Notes

This project uses Django's built-in authentication system and stores uploaded media in the `media/` folder.
