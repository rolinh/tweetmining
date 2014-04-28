# ABOUT

This is a small project related to a data mining course given by Dr. Alexandros
Kalousis at the University of Geneva, Department of Computer Science.

Project goals are detailed in `doc/project-goals.pdf`.

Briefly, the goal is to collect and analyze data gotten from the Twitter
microblogging system and build a model to predict if a tweet will be retweeted
or not, i.e. to predict if a tweet can be considered as popular or not insight a
community.

# SETUP

This project uses `python` 2.7 thus  you obviously need it.
`pip` and `virtualenv` are the recommended way to install all the required
libraries in order to keep everything clean.
To build the required packages, you also need `gcc` (or another C-compiler),
`gcc-fortran` (or another Fortran compiler) and `swig`.
Once the requirements are met, you can process as follow:

* Set up a virtual environment first:
  `virtualenv -p python2.7 env`
* And activate it:
  `source env/bin/activate`
* Then, to install the required libraries, issue the following commands:
  `pip install numpy`
  `pip install -r requirements.txt`

And you should be all set. Note that `numpy` needs to be installed beforehand
otherwise `matplotlib` and `scipy` will not build.

# FETCH NEW DATA

Create a twitter app developper account. Then, rename
`scripts/credentials.py.sample` to `scripts/credentials.py` and modify the
credential values for valid ones.

You can adapt search tag, language and output json file from
`scripts/fetch_data.py` and then run the file to fetch a dataset.

Remember that, as of Twitter API v1.1, API is limited and you will only be able
to fetch a certain amount of data at once. Run the script several times on a
several days period if you want to fetch enough data. Also remember that using
free Twitter API, you can only fetch information in from a limited time period
and not trough all Twitter history. You gotta pay for it if you want more... :(
