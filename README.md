fractal-castle
==============

Install Python 2.7.

Download py script for creating virtual enviroment from https://raw.github.com/pypa/virtualenv/master/virtualenv.py and
put it in the folder where project will be stored.

Create virtual enviroment within project folder typing in cmd/terminal $ python virtualenv.py flask
This command creates a complete Python environment inside the flask folder.

Initialize git with $ git init 

Clone no-db branch of this project 
you can do it with $ git clone -b no-db --single-branch https://github.com/4toblerone/fractal-castle.git

After you are done with cloning remote repo , inside your project folder find requirements.txt file and move it to
flask/Scripts folder if you are using Win and if you are using OSX it should flask/bin .
requirements.txt contains necessary dependencies.

Install previously metioned dependecies. Position your self again in your project folder and type :

(for Win users) flask\Scripts\pip install -r requirements.txt

(for OSX users) flask/bin/pip install -r requirements.txt


After this your enviroment should be all set. 

