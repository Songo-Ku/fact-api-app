Description
Django REST API app with basic functionalities:
Access to facts_dates db. User can list/post/delete dates month and day to fetch fun fact for selected particular date. Dates are validated with real calendar. 
Check popularity ranking of saved/selected dates and facts in db. We can see count of all post data and id is specified in desc way depend on amount of days_checked. 

Installation
Prerequisites
Python
Django / Django REST Framework
Docker
PostgreSQL

Setup
Clone repository and fill .env file placed in root directory, with variables:
SECRET_KEY - django secret key
DATABASE_URL - postgres database url
Run in root directory docker-compose up
