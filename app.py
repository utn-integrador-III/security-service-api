# Call external libraries
from pymongo import MongoClient, errors
from flask import Flask, jsonify, abort, make_response, request

# Create default flask application
app = Flask(__name__)

# ================================================================
# D A T A A C C E S S C O D E
# ================================================================
# Create connection with MongoDb

def contextDB():
    try:
        conex = MongoClient(
            host='mongodb+srv://db-mongodb-nyc1-88903-b647ee80.mongo.ondigitalocean.com',
            username='doadmin', password='15fec6A2m890NI4n',
            serverSelectionTimeoutMS=5000  # 5 seconds timeout
        )
        # Attempt to retrieve server information to check connection
        conex.server_info()
        return conex
    except errors.ServerSelectionTimeoutError as err:
        print(f"Error connecting to MongoDB: {err}")
        return None

DBconex = contextDB()

# ================================================================
#                 A P I R E S T F U L S E R V I C E
# ================================================================
# -----------------------------------------------------
# Error support section
# -----------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request....!'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized....!'}), 401)

@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Forbidden....!'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found....!'}), 404)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal server error....!'}), 500)

# Get Aircraft
@app.route('/', methods=['GET'])
def Help_Route():
    try:
        # Check connection status
        DBconex.server_info()
        salida = {
            "status_code": 200,
            "status": "Connection Ok",
            "data": []
        }
    except errors.ServerSelectionTimeoutError:
        abort(500)  # Return 500 Internal Server Error if DB connection failed
    return jsonify({'data': salida}), 200

# -----------------------------------------------------
# Create thread app
# -----------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
