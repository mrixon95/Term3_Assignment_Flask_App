# ConnectIT: Connecting IT professionals

My app is designed to be similar to LinkedIn but for IT professionals.
On ConnectIT, IT professionals will be able to:

* register as a user and add photos
* like and comment on user posts
* add work history, study history, certifications and links to their resume/projects
* write down meetings they have

Docs for my app:
* [Trello board](https://trello.com/b/7Y9qhmBJ/project-management)
* [Swagger editor yml](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/mrixon95/Docs_On_Term3_CCC_course/main/LinkedIn%20App/connectITAPI.yaml)




# Wireframes

### Login page
![Login_Page_Wireframe](docs/Login_Page_Wireframe.jpg)

### Profile page
![Profile_Page_Wireframe](docs/Profile_Page_Wireframe.png)

### Activity Feed page
![Activity_Feed_Wireframe](docs/Activity_Feed_Wireframe.png)

### Diary page
![Diary_Page_Wireframe](docs/Diary_Page_Wireframe.png)

### Salary data page
![Salary_Page_Wireframe](docs/Salary_Page_Wireframe.png)


### Settings page
![Setting_Page_Wireframe](docs/Setting_Page_Wireframe.png)

### Proposed Entity Relationship Diagram

* Each User can have multiple images, certifications, work histories, connections, meetings, messages, study histories, resume/projects, posts, comments and like multiple posts
* Each Like belongs to one post and one user
* Each comment belongs to one post and one user
* Each connection has one user who requests the connection and one user who can decide to confirm it



![Entity_Relationship_Diagram](docs/ERD_diagram.png)


## Installation
In order to install this application:

1. Install python 3.8, python3.8-venv and python3-pip on your system.
   On Ubuntu run ```sudo apt install python3.8 python3.8-venv```
   Verify that it install successfully by running ```python3.8 --version```

2. Install pip3 the python3 package manager.
   On Ubuntu run ```sudo apt-get install python3-pip```
   or ```python3 -m pip install pip```

3. Clone the application onto your system by running ```git clone https://github.com/mrixon95/Docs_On_Term3_CCC_course.git```
   and cd into the directory

4. Download a virtual environment and activate it.
   On Ubuntu run ```python3 -m venv venv``` to download the module
   and ```source venv/bin/activate``` to activate the virtual environment.
5. install application dependencies within the activated Python3.8 virtual environment by running ```pip3 install -r requirements.txt```.


## Setup
Create a ```.env``` file using the ```.env.example``` template within the ```src``` folder and populate the required fields within the ```.env``` file.

## Custom Commands
These following flask commands below are for automating tasks related to database tables and for testing during the development phase.
1. ```flask db create```: creates database tables defined in registered models.
2. ```flask db seed```: populates database tables with dummy data using faker module.
3. ```flask db drop```: drops all database tables defined in registered models.



# CI/CD Pipeline



There are the steps required as part of the continuous integration workflow when pushing modified code to Github. File reference ci-cd.yml file

1. The test_suite job will run on one of GitHub's VMs using the latest Ubuntu operating system. The new code pushed to github is checked out into this VM.
2. The VM installs python3.8 and installs the dependencies. These dependencies and their version number are written on seperate lines in the requirements.txt file.
3. The automated tests in the tests directory are ran 
4. The .py files are checked against the PEP8 style guide by running flake8