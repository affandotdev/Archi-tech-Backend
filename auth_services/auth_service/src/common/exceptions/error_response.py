def error_response(message, status_code=400):
    return {
        "status": "error",
        "message": message,
        "status_code": status_code
    }
