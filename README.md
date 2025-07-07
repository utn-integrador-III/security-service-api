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


## Running the project in a docker container



1. create .env file take the variables from [.env.example](.env.example) and update the values.

2. Create the image container ``` docker build -t unt-img-security-api . ```

3. Create and run the container: 

``` docker run -d -p 5002:5002 --name utn-security-api --env-file .env utn-img-security-api ```

5. Now you can access the api by default in this url: <http://localhost:5002>