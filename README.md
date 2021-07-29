# Django Random News

### How to run the project
1. Ensure the following python library is installed in your computer
```
newsapi-python
Django
```

2. Make migration for the website app
```
python manage.py makemigrations website
python manage.py migrate
```

3. To run the web app
```
python manage.py runserver
```

### What this project does
User will be able to
1. Login and logout
2. Click on generate news button to random pulls a recent article text from a random news outlet
3. Specify what category of news they are interested in
4. View list of articles viewed in the past