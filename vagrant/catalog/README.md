# About the Project

This is the second project in the Udacity fullstack developer nanodegree program.

The task was to create a catalog application where users can view, create, update and delete
items. The catalog needed to have a third party sign-in/sign-out feature along with local
user permissions. I chose to place my local user permissions around the create, update and delete
functionality.

# What is Needed to Complete the Project

The following need to be installed:

1.  Vagrant
2.  Virtual Box
3.  Python 2.7.10

# The Following Needs Cloned From Github

1. [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)

# Steps to Start the Application

In your terminal `cd` into the fullstack-nanodegree-vm directory and run the `vagrant up`
command. Once this step is complete run the `vagrant ssh` command and `cd` into the shared
vagrant file using `cd /vagrant`.

To setup the database run `python catalog_db_setup.py`
To populate the database run `python db_items.py`

# Run the Main Flask File
Now you can run the main flask application file in the terminal using `python flask_catalog.py`
This should start the application on port 5000 and can now be used in your web browser by visiting
`http://localhost:5000/activities/home` to see the home page.
