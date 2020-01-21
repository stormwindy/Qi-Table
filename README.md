# Qi-Table

Main repo for SDP at University of Edinburgh

## Units & Code Standards

Distance should be in meters *always*, and angles should be in radians.

We'll be sticking as close to [PEP8](https://www.python.org/dev/peps/pep-0008/)
as is reasonable. Basically, *spaces instead of tabs*.

## Software Setup

To get started:

```
$ git clone https://github.com/stormwindy/qi-tables
$ cd qi-tables
$ virtualenv env_qi -p python3
$ source activate env_qi/bin/activate
$ pip install -r requirements.txt --verbose
```

N.B. We'll be using virtual environments to avoid polluting your global python
install and to ensure we're all running the same version of Python.

Base classes for the table/chairs are in `./base.py`. These should be used
wherever possible to maintain code interoperability.

