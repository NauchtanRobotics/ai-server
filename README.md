# ai-server

The vision for *ai-server* is a django project that provides an end-point 
where you can post images to for AI classification.  Detections are returned 
as json data in the html response.

Optionally, the images posted can be stored for potential use as training data.

This project is in the early stages of development and is only a skeleton at 
this stage.

## Installation

### 1. Library Dependencies

Create a virtual environment, activate it and run `pip install -r requirements.txt`

### 2. Environmental Variables

Set environment variable RACAS_IMAGES_ROOT for the folder
location in which you would like images to be stored.

In Linux/Ubuntu edit ~/.bashrc adding a line:

<code>
export RACAS_IMAGES_ROOT=/home/userX/root_folder_name
</code>

replacing <userX> with the login name which will be running when
serving the endpoint. Replace <root_folder_name> with whatever 
string you like, adding folder depth as required.

In Linux, edit this file by running this command in a terminal
`nano ~/.bashrc` 
and paste in the line of code above. CTRL-X to save and exit,
then execute 
`source ~/.bashrc` 
to make sure the effects are immediate without having to reboot.
At this stage you will probably need to reactivate your virtual
environment.

### 3. Configuration File
Create a file to store configuration data including data that should 
not be stored in the repository for security reasons. At a minimum
the file should include the following:

<pre>
[SECURITY]
SECRET_KEY = our secret key
</pre>

Tip: Do not add quotation marks around any of the values stored in config.ini.

In Linux, create config.ini into the right location by moving into the project
root and using this command:

<code>
nano ai_server/ai_server/config.ini
</code>

and paste in the contents above, save and exit via CTRL-X.

DO NOT COMMIT config.ini to your repository, even if stored
in a private repository on github.com

### 4. Running the Server 

Django provides some tools for running the server to allow code
development and testing in an isolated dev environment - i.e.
that is, isolated from security threats in the world-wide web.

Alter the file ai_server/ai_server/settings.py if required, 
such as adding 'localhost' to the list for ALLOWED_HOSTS.

To run the server, activate your virtual environment and run these 
commands:

<code>
cd ai_server

python manage.py runserver 0.0.0.0:8000
</code>

See django documentation for more detail.

### 5. Running the Server in Production

Extra security measures are required including installation of web server 
software (apache or NGINX) and a web gateway interface (wsgi, e.g. gunicorn)
which are production grade components. Do not use the django features 
provided for development environments. See django documentation for all 
details. 


## Changelog

* ISS-0002 - Added installation instructions to README.md
* ISS-0001 - Skeleton code accepts a single image and saves to disk.

