# ABOUT

This is a small project related to a data mining course given by Dr. Alexandros
Kalousis at the University of Geneva, Department of Computer Science.

Project goals are detailed in doc/project-goals.pdf.

Briefly, the goal is to collect and analyze data gotten from the Twitter
microblogging system and build a model to predict if a tweet will be retweeted
or not, i.e. to predict if a tweet can be considered as popular or not insight a
community.

# SETUP

This project uses python 3. Therefore, you obviously need python 3,
pip and virtualenv are the recommended way to install all the required libraries
in order to keep everything clean.


So you first need to install pip and virtualenv if they are not already
installed on your system.

Set up a virtual environment first:

    virtualenv --no-site-packages .

And activate it:

    source bin/activate

Then, to install the required libraries, issue the following
command:

    pip install -r requirements.txt

And you should be all set.

<!-- vim: set filetype=markdown textwidth=80 -->
