# Item Catalog

This item catalog web application provides a list of items within a variety of categories and integrate third party user registration and authentication. And authenticated users should have the ability to post, edit, and delete their own items. Also, it provides JSON endpoints information.


## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Instructions](#instructions)
- [Support](#support)


## Features

* Show all the added catalogs and the latest added catalog items;
* Selecting a specific category shows you all the items available for that category.
* Selecting a specific item shows you specific information about that item.
* Provide third party user registration and authentication. After logging in, a user has the ability to add, update, or delete item information. However, an user cannot add, update or delete any catalogs or items that are created by other users.
* Provide JSON endpoints for catalogs information and catalog items.




## Requirements

- Download [python(version2.7)](https://www.python.org/downloads/) on your computer;
- Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) on your computer.
- Get this web application's source code from Git.
- Launch the Vagrant VM (by typing vagrant up in the directory fullstack/vagrant from the terminal). Once it is up and running, type vagrant ssh. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type exit at the shell prompt. To turn the virtual machine off (without deleting anything), type vagrant halt. If you do this, you'll need to run vagrant up again before you can log into it.
- Install the necessary packages: type 'sudo pip install flask==0.9' in the command line to install Flask(version 0.9) and also install oauth




## Instructions
- After you have Vagrant up and running type vagrant ssh to log into your VM. change to the /vagrant directory by typing cd /vagrant. This will take you to the shared folder between your virtual machine and host machine.
- Type ls to ensure that you are inside the directory that contains project.py, database_setup.py, and two directories named 'templates' and 'static'
- Now type python database_setup.py to initialize the database.
- Type python lotsofcatalogs.py to populate the database with catagories and catalog items.
- Type python project.py to run the Flask web server. In your browser visit http://localhost:8000 to view the item catalog app. You should be able to view all the catalogs and related item information.
- To login, simply click the "click here to login" button in the right top conner of the website, and it provides google+ sign in and facebook sign in. Choose the login method you like, it will direct you to the respected login page. After successful login, you are able to add, update or delete your own catalogs or catalog items. However, if you try to add, delete any catalogs or catalog items that were created by others, your will receive an alert message.
- In your browser, visit http://localhost:8000/catalog/JSON to obtain the JSON endpoints for catalog information and visit http://localhost:8000/catalog/catalog_id/JSON to get the JSON endpoints for item information about a specific catalog.


## Support

If you have any issues about the Item Catalog web application, please let me know.
My email address is yanhong.zhou05@gmail.com.