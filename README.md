# Automatic screencast

PoC of autogenerating webapp screencasts, using Python and Selenium.

## Install system-wide requirements

You're going to need:

- Python 2.7
- virtualenv
- recordmydesktop
- Xvfb


## Install Python requirements

Create a virtualenv:

```
% virtualenv --python /usr/bin/python2.7 venv
% . venv/bin/activate
% pip install pip-tools
% pip-sync requirements.txt
```

Or simply:

```
make setup
```

## Build the thing

```
make
```

Then visit ``./output/index.html`` in your browser.
