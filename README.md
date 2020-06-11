# Project
Bitmex RESTful and WS API implementation 

## Getting started
### Prerequisites
Pipenv should be installed to use app
```shell script
pip install pipenv
```

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

Put API_KEY and API_SECRET in corresponding fields in Admin panel

### Project is available at:
RESTful API:
```
http://localhost:8888/api/
```

For example, to retrieve orders for account make such request
```shell script
GET http://localhost:8888/api/orders/?account=<your_account_name>
```

WebSocket API:
``` 
ws://localhost:8888/ws/bitmex_api/<your_account_name>/
```
