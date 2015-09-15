# Supporters: Python Twilio Example
An example of signing up new Supporters using The Groundwork API through SMS and a Flask Application

  Have a Heroku account? Try this example on a live web server with →
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## What's here?

- ``/setup.py`` - Setup script for the project/application. See [notes](#setuppy)
- ``/requirements.txt`` - See [notes](#requirementstxt).
- ``/supporters_twilio``
- ``/supporters_twilio/__init__.py`` - where `__version__` is set
- ``/supporters_twilio/config.py`` - configuration
- ``/supporters_twilio/application.py`` - main application code
- ``/supporters_twilio/wsgi.py`` - wsgi module

#### setup.py

Python packaging is interesting to say the least. Writing a setup script can be confusing. The basics are laid out here and should get you 90% of the way. Check out the [official documentation](https://docs.python.org/2/distutils/setupscript.html) if you get stuck.

#### requirements.txt

All dependency resolution should be handled in ``setup.py``. This ``requirements.txt`` file is here due to the old pattern that is entrenched in the Python world. The contents of this file (``-e .``) will allow developers to use the familiar ``pip install -r requirements.txt``.

## Local Development
Making modifications and running this project locally requires a number of steps.

#### Prerequisites && Assumed Technologies
- Python
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) and [Virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html)

#### Recommended Setup

_Step 1: Get the code:_
```
git clone git@github.com:tylergaw/supporters-python-twilio.git
cd supporters-python-twilio
```

_Step 2: Make and set up virtual env_

If you're unfamiliar with virtualenvs, don't fret. Virtualenvs are just a fancy way of making sure your Python project dependencies stay separated.

```
mkvirtualenv supporters-python-twilio
deactivate
```
The app needs a number of env vars to function. Instead of manually setting those each time, we'll leverage Virtualenvwrapper.

In the repo is [.env.example](https://github.com/tylergaw/supporters-python-flask/blob/master/.env.example) that specifies the needed env vars. Use a text editor of your choice to update your `postactivate` and `postdeactivate` virtualenv hooks.

```
vim ~/.virtualenvs/supporters-python-twilio/bin/postactivate

export ENV=local
export GW_API_URL=https://api.url.com/ #trailing slash here please
export GW_CLIENT_ID=<client_id>
```

and be sure to unset any vars when leaving the virtualenv

```
vim ~/.virtualenvs/supporters-python-twilio/bin/postdeactivate

unset ENV
unset GW_API_URL
unset GW_CLIENT_ID
```

and finally, reactivate your newly minted virtualenv

```
workon supporters-python-twilio
```

_Step 3: Install the Python Dependencies_
```
make setup
```

_Step 4: Run the local server_
```
make run
```

If all is well, the site will be available at [http://localhost:5000](http://localhost:5000)
