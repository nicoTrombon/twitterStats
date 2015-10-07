Twitter Stats app
===============

A prototype app which demos interaction with the twitter API.
Type in a user screen name or id and you will get some simple
stats of the account and most common hashtags used.
Examples of output in examples folder.

Getting Started
---------------

### Initial Setup ###
1. Make a new virtualenv: ``virtualenv env``
2. Activate the virtualenv: ``source env/bin/activate``
3. Install Flask: ``pip install Flask``
4. Install Tweepy: ``pip install Tweepy``
5. Edit ``get_stats.py:10-13`` with your twitter api credentials
6. Run the app: ``python app.py``
7. Open website in browser at ``http://127.0.0.1:5000/``
