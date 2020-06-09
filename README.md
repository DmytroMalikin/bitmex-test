# Project
Bitmex RESTful and WS API implementation 

## Getting started
### Installation
```shell script
pipenv install
```

### Running
```shell script
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8888
```

### Create bitmex account
Create test account for bitmex at http://localhost:8888/admin
Account name will be used for api requests.

### Project is available at:
RESTful API:
```
http://localhost:8888/api/
```

WebSocket API:
``` 
ws://localhost:8888/ws/bitmex/<account_name>
```
