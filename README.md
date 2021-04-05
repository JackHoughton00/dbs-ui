The template for this project was adapted from the following links: 
    https://www.youtube.com/watch?v=w25ea_I89iM
    https://github.com/bradtraversy/python_feedback_app/blob/master/templates/index.html

These two links were used as the foundation for the webapp. Some chunks of code were directly sourced 
from the GitHub repository, but the overall project had to be modified for our groups needs. 


IMPORTANT NOTE: 

In order to connect to the database you will need to go to line 17 on app.py and enter your login credentials
as you normally would when signing into pgAdmin4. Without this step being followed the web app will not be functional. 

The instructions to run the webapp will also be in the file called README.txt. In order to run the program you will first need to run the following lines of code:
	1. pip install pipenv 
	2. pipenv shell
	3. pipenv install flask 
	4. pipenv install pyscopg2 (installing this package and be finicky, if it cannot install then the next line should be sufficient enough)
	5. pipenv install pyscopg2-binary
	6. pipenv install flask-sqlalchemy
	7. pipenv install gunicorn
	8. python app.py

From line two onwards the installations should be done in the pipenv shell, the website may not work otherwise. Assuming everything was successful you should now be able to open the website locally in a browser. The website should be viewable if you type the following in the search bar, “http://127.0.0.1:5000/”. If this link does not work, please check your terminal and use the port listed there. A picture has been provided for reference on page 6 of report.pdf
After all of the steps have been followed, the website should now be functional and able to receive inputs from the user. 









