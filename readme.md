Description:

    drf app with two functionalities. First let access to db dates_facts. User can use actions: list, delete, post. 
    Dates fill by user are valideted with real calendar. Facts are generate automatically via 3rd pt api numbersapi. 
    Second generate view with popular ranking of months. User can see checked_days grouped by month. 

Installation

Prerequisition:

    Python
    Django / Django REST Framework
    Docker
    PostgreSQ

Setup:

    1. Clone repository and fill .env file placed in root directory, with variables:
        SECRET_KEY - django secret key
        DATABASE_URL - postgres database url
    2. Run in root directory docker-compose up

