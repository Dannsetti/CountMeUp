# CountMeUp
Exercise Assignment  

This program is a web application that simulate a live elections results.

To run the program, first you have to download mongodb because the database used in this application use it

https://www.mongodb.com.

Also have to install flask, pymong and numpy as they are libraries that I used for the backend, tests and main scenarios:

To install it run from the terminal the following command:

pip3 install pymongo
pip3 install flask
pip3 install numpy

After everything is installed you can run the web application through the terminal using:

python3 app.py

But first run start the mongo data base:

brew services start mongodb

And in case you need to restart it:

brew services restart mongodb

And then access the following link:

http://localhost:5000/

run app

Then to see the required main scenario run from the terminal the CountMeUp.py file:

python3 CountMeUp.py

Go to the provided web link and enjoy :)

Extra Notes: 

- There are many tests scenarios in the tests folder, some of them are to be executed in the IDLE or terminal Shell and the other using the link. Note that not all of them may be working or may not get the right ouput, I used for tests pruposes.

- In case that you wanna try to run to see other solutions, you have to delete the database crated by running in the terminal:

python3 deleteDataBase.py

And then refresh the webpage.
