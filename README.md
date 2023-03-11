# Casting Agency Capstone Project

## Udacity Full Stack Nanodegree

The Casting Agency primarily responsibility is to supervise and manage the entire process runs smoothly and efficiently. With a team of skilled professionals, the Casting Agency works tirelessly to oversees the production of movies and the allocation of actors to those films. 

The primary goal of this project is to develop a back-end application that showcases the functionality of endpoints using Role Based Access tests. To achieve this objective, the project incorporates JWT authentication, and pre-existing JWT's are available for testing. The project aims to exhibit my proficiency in implementing authorization tools, RBAC endpoints, error handling, test writing, and effectively managing data between the front-end and back-end of the application.

The Casting Agency has three roles within its system: the Casting Assistant, the Casting Director and Executive Producer. This strict demarcation of roles and their corresponding permissions ensures that all activities within the system are carried out by the appropriate personnel, reducing the risk of unauthorized access and errors.

### Project Setup

The project's backend is developed using Flask (Python3) and postgres database (psql). To run the project, pip is required to install the dependencies.

```python
pip install -r requirements.txt
```

It is encouraged to use Python virtual environment as;

```python
python3 -m venv env
source env/bin/activate
```

In the project directory, the file `setup.sh` is used to export the required key-value pairs to the environment variables.

```bash
chmod +x setup.sh
./setup.sh
```

This will export the JWT's for two roles: Casting Director and Exective Producer. Also, it will export the database url. I am using postgres on AWS RDS for the models.

`
mydb.cnemmrnwnpsd.us-east-1.rds.amazonaws.com
`

### Server Deployment and Authentication

I have hosted the application on Heroku. The public URL for which is:

[kpitb-capstone.herokuapp.com/](https://kpitb-capstone.herokuapp.com/)

The project uses Auth0 based accounts for the users and to use the RBAC roles. In case the provided JWTs are expired, new JWTs can be created by visiting the following URL.

[Click to create new JWTs](https://aafsnd.us.auth0.com/authorize?audience=fsnd_casting_agency&response_type=token&client_id=YyU9ZuiLzjPmlH8FZqwyasPhDO5tQWJf&redirect_uri=http://localhost:5000/)

The login details for the three users are:

1. Casting Assistant:
Email: `castingassist@agency.com`
Pass: `Abcd1234.`

2. Casting Director:
Email: `castingdirector@agency.com`
Pass: `Abcd1234.`

3. Exective Producer:
Email: `executiveproducer@agency.com`
Pass: `Abcd1234.`

The JWTs can be copied from the URL and pasted into the `setup.sh` file.

### Testing

To run the tests, please do as follows.

```bash
python test_app.py
```

There are a total of 18 tests. 
