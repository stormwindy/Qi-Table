# Qi-Table

Main repo for SDP at University of Edinburgh

## Units & Code Standards
Distance should be in meters *always*, and angles should be in radians.

### Python
We'll be sticking as close to [PEP8](https://www.python.org/dev/peps/pep-0008/)
as is reasonable. Basically, *spaces instead of tabs*.

### C/C++
Suggested coding standard follows ["Embedded C Coding Standard"](https://dl.dropbox.com/s/bu4nq51qvk5uzzh/barr_c_coding_standard_2018.pdf?dl=0).

## Software Setup

To get started:

```
$ git clone https://github.com/stormwindy/qi-table
$ cd qi-table
$ virtualenv env_qi -p python3
$ source env_qi/bin/activate
$ pip install -r requirements.txt --verbose
```

For venv:
```
$ git clone https://github.com/stormwindy/qi-table
$ cd qi-table
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt --verbose
```

N.B. We'll be using virtual environments to avoid polluting your global python
install and to ensure we're all running the same version of Python.

Base classes for the table/chairs are in `./base.py`. These should be used
wherever possible to maintain code interoperability.

## App Setup

The frontend is currently using https://create-react-app.dev/ and is not hosted on the server that it communicates with.

To start the app:

```
$ cd app
$ cd my-app
$ npm start
```
To connect, open localhost:3000 in your browser, though it should open automatically. For the app to function correctly, you need to also start the server:

```
$ source env_qi/bin/activate
$ cd app
$ flask run
```
This will open the server at localhost:5000, though you don't need this information to use the app

Note that there is currently no way to delete layouts from the database. You can do this manually by opening layouts.db in sqlite3 (this should come installed on Mac, not sure about Windows):

```
$ cd app
$ sqlite3 layouts.db
```

If you know SQL feel free to play around with it. If you just want to delete the saved layouts:

```
>>> delete from positions;
>>> delete from layouts;
```


