from flask import Flask
from marshmallow.exceptions import ValidationError
from init import app
from blueprints.cli_bp import db_commands

app.register_blueprint(db_commands)

@app.route("/")
def hello():
  return "Hello World!"

@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    return {"error": "Not Found"}, 404

@app.errorhandler(ValidationError)
def invalid_request(err):
    return {"error": vars(err)["messages"]}, 400

@app.errorhandler(KeyError)
def missing_key(err):
    return {"error": f"Missing field: {str(err)}"}, 400

print(app.url_map)
