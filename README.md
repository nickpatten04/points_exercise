# points_exercise

To start the service, you can just app.py. To test the routes, you can download an application call "Postman" and send requests to each of the routes in localhost. The routes and associated methods are listed in the @app.route() decorators in app.py

## Formats for POST methods:

- /users = {"first_name: \<string\>, "last_name": \<string\>}
- /users/<user_id>/transactions = {"payer": \<string\>, "points": \<int\>, "timestamp": \<string\>} __\*__
- /users/<user_id>/points = {"points": \<int\>"}
  
  

## Notes
- __\*__ timestamp must be a string in python isoformat
