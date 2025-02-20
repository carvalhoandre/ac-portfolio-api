from flask import jsonify

def standard_response(success, message, status_code, data=None):
    response = {
        "success": success,
        "message": message,
        "Access-Control-Allow-Origin": 'http://localhost:8080',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code
