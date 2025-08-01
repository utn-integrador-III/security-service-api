# security-service-api

> <http://localhost:5002>

1. create virtual env: `python3 -m venv venv`
2. create .env file
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
