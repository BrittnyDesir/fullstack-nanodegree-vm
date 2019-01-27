# About the Project

This is the first project in the Udacity fullstack developer nanodegree program.

There are three questions that are required to be answered. The questions are as follows:

1.  What are the most popular three articles of all time?
2.  Who are the most popular article authors of all time?
3.  On which days did more than 1% of requests lead to errors?

The task is to use SQL queries to extract the data that answers these questions.
The queries are written in SQL and Python is used to connect to the database,
run the queries and output the answers. I then saved the output in a .txt file.

# What is Needed to Complete the Project

The following need to be installed:

1.  Vagrant
2.  Virtual Box
3.  Python 2.7.10

The following repo needs cloned from Github:

1.  [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)

Using the terminal `cd` into the directory and inside, you will find another directory called vagrant.
Change directory to the vagrant directory. From here run the command `vagrant up`. Once the install
is complete run the command `vagrant ssh`. The shell prompt should begin with the word vagrant.

Now change directory to the shared vagrant directory by entering the command `cd /vagrant`. This is where the
PostgreSQL database server we are using is located for the project.

Next, download the data for the database and unzip the file:

 1\.[Data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Put the file called `newsdata.sql` into the vagrant directory. Make sure the file is in the correct place, then
load the data into the database using the command `psql -d news -f newsdata.sql`.
Use `psql -d news` to connect to the database.

# Information About the Database

The database has the following 3 tables:

1.  authors
2.  articles
3.  logs

# Creating Views
In order to answer the last question I created two views so the tables and query are easier to follow. The first view creates a table view called requests and shows the total number of requests per day. To create the view enter in the following command:

`create view requests as select count(*) as totalrequests, cast(time as date) as perday from log group by perday;`

The second view creates a table called errors that shows the total number of requests that resulted in an error per day. To create the view enter the following command:

`create view errors as select count(*) as totalerrors, status, cast(time as date) as day from log where status like concat('%', 404, '%') group by status, day order by day;`

# Run the Python File
Now run the python file that contains the queries by entering the following command:

1. `python logs_analysis_project.py`
