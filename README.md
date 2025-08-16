# Security Service Api

## Running the project locally via VS Cod

1. create virtual env: `python3 -m venv venv`
2. create .env file take the variables from [.env.example](.env.example) and update the values.
3. run pip3 install -r requirements.txt
4. If you are using vs code, go to `run and debug` and create a launch.json file and add the following (for env file, copy your path and paste it):
   { "version": "0.2.0",
   "configurations": [
   {
   "name": "Python: Current File",
   "type": "debugpy",
   "request": "launch",
   "program": "./app.py",
   "console": "integratedTerminal",
   "envFile": ".env"
   }
   ]
   }

5. Run the project under 'Run and debug'

## Sending emails with Azure Communication Services (ACS)

1. Replace these variables in the .env file.

```.env
# --- Azure Communication Services ---
EMAIL_PROVIDER=acs
ACS_CONNECTION_STRING=endpoint=https://security-acs-dev.unitedstates.communication.azure.com/;accesskey=F9GMca2OUAYjw6vHJK5PS5MjJv8iTzHzCdTapttFPJ6rKub3fCbcJQQJ99BHACULyCplF0bbAAAAAZCSDMEO
ACS_SENDER_ADDRESS=DoNotReply@6315dc5b-c4e5-4897-9694-d69302c913ac.azurecomm.net
# (opcional) Si se desea utilizar un correo alternativo para las respuestas
# REPLY_TO_EMAIL=DoNotReply@6315dc5b-c4e5-4897-9694-d69302c913ac.azurecomm.net
```


## Running the project in a docker container



1. create .env file take the variables from [.env.example](.env.example) and update the values.

2. Create the image container ``` docker build -t unt-img-security-api . ```

3. Create and run the container: 

``` docker run -d -p 5002:5002 --name utn-security-api --env-file .env utn-img-security-api ```

5. Now you can access the api by default in this url: <http://localhost:5002>