# Django Random News

### Deployment
Project is deployed on heroku at this link https://django-random-news.herokuapp.com/

### How to run the project
1. Ensure the following python library is installed in your computer
```
newsapi-python
Django
```

2. Obtain a api key from https://newsapi.org/ and place it into apiKey.py in 'website' app

2. Make migration for the website app
```
python manage.py makemigrations website
python manage.py migrate
```

3. To run the web app
```
python manage.py runserver
```

### Distinctiveness and Complexity
User will be able to
1. Login and logout
2. Click on generate news button to random pulls a recent article text from a random news outlet
3. Specify what category of news they are interested in
4. View list of articles viewed in the past
5. Delete article from history

### Files and directory
- `RandomNews` - project directory
- `Website` - Main app directory
    - `static\website` - Contains all the static files 
        - `script.js` - Contains the js codes
    - `templates\website` - Contains all the html files
        - `index.html` - Main page for the website
        - `layout.html` - Template for the website
        - `login.htmml` - Contains the template for logging in
        - `navbar.html` - Inserted into layout.html for the navbar
        - `register.html` - Contains the template for registering
    - `admin.py`: added models here to access in admin page
    - `apiKey.py`: Contains the API key for newsAPI
    - `models.py`: Contains the models for this project
    - `urls.py`: Contains the URL routes 
    - `views.py`: Contains the function for the views
- `Requirements.txt`: Contains all the necessary library and their version