from flask import Flask, request, jsonify

from module.constants.users import USERS_TABLE
from module.constants.transactions import TRANSACTIONS_TABLE
from module.transaction import Transaction
from module.user import User


app = Flask(__name__)


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(**data)
    USERS_TABLE.add(new_user)
    return jsonify(USERS_TABLE.find_row(USERS_TABLE.rows[-1]._id).to_dict(dates_to_string=True)), 201


@app.route("/users")
def get_users():
    return jsonify({"users": [user.to_dict(dates_to_string=True) for user in USERS_TABLE]}), 200


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = USERS_TABLE.find_row(user_id)
    if not user:
        return jsonify({"message": "User does not exist."}), 404
    return jsonify(user.to_dict(dates_to_string=True)), 200


@app.route("/users/<int:user_id>/transactions")
def get_transactions_for_user(user_id):
    return jsonify({"transactions": [trs.to_dict(dates_to_string=True) for trs in TRANSACTIONS_TABLE if trs.user_id == user_id]}), 200


@app.route("/users/<int:user_id>/balance details")
def get_balance_details_for_user(user_id):
    user = USERS_TABLE.find_row(user_id)
    if user:
        return jsonify(user.balance_details), 200
    else:
        return jsonify({"message": "User does not exist in table"}), 404


@app.route("/transactions")
def get_all_transactions():
    return jsonify({"transactions": [trs.to_dict(dates_to_string=True) for trs in TRANSACTIONS_TABLE]}), 200


@app.route("/users/<int:user_id>/transactions", methods=["POST"])
def log_transaction(user_id):
    data = request.get_json()
    data["user_id"] = user_id
    validated_transaction = TRANSACTIONS_TABLE.add(Transaction(**data))
    if validated_transaction:
        return jsonify(TRANSACTIONS_TABLE.find_row(TRANSACTIONS_TABLE.rows[-1]._id).to_dict(dates_to_string=True)), 201
    else:
        return jsonify({"message": "The user you are trying to log a transaction for does not exist. Please add the "
                                   "user first, then log the transaction."}), 404


@app.route("/users/<int:user_id>/spend", methods=["POST"])
def spend_points(user_id):
    points_to_spend = request.get_json()["points"]
    user = USERS_TABLE.find_row(user_id)
    points_remaining = user.spend_points(points_to_spend, TRANSACTIONS_TABLE)
    if points_remaining == -1:
        return jsonify({"message": "User wants to spend more points than they have available."})
    else:
        return jsonify(user.balance_details), 201


if __name__ == "__main__":
    app.run(debug=True)
