if [ -f .env ]; then
    # Load Environment Variables
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi
gunicorn --reload --log-level 'debug' -t 3600 -b :${SECURITY_SERVICE_PORT} run_server:App