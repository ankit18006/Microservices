import os
from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

USER_SERVICE_URL = os.environ.get("USER_URL", "https://micro-user-xxxxx.onrender.com")
ORDER_SERVICE_URL = os.environ.get("ORDER_URL", "https://micro-order-xxxxx.onrender.com")

@app.route('/')
def index():
    return render_template('index.html')

# ... baaki sab routes yahi niche hongi ...

    try:
        users = requests.get(USER_SERVICE_URL).json()
    except:
        users = []

    selected_user = None
    orders = []

    return render_template(
        'index.html',
        users=users,
        orders=orders,
        selected_user=selected_user or {'id': '', 'name': 'User'}
    )


@app.route('/api/users', methods=['GET', 'POST'])
def users_api():
    if request.method == 'GET':
        r = requests.get(USER_SERVICE_URL)
        return jsonify(r.json())
    else:
        data = request.get_json()
        r = requests.post(USER_SERVICE_URL, json=data)
        return jsonify(r.json())


@app.route('/api/users/<int:user_id>', methods=['PUT', 'DELETE'])
def user_update_delete(user_id):
    if request.method == 'PUT':
        data = request.get_json()
        r = requests.put(f"{USER_SERVICE_URL}/{user_id}", json=data)
        return jsonify(r.json())
    else:
        r = requests.delete(f"{USER_SERVICE_URL}/{user_id}")
        return jsonify({"deleted": True})


@app.route('/orders/user/<int:user_id>')
def get_orders(user_id):
    try:
        r = requests.get(f"{ORDER_SERVICE_URL}/user/{user_id}")
        return jsonify(r.json())
    except:
        return jsonify([]), 404


@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    r = requests.post(ORDER_SERVICE_URL, json=data)
    return jsonify(r.json())


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    r = requests.delete(f"{ORDER_SERVICE_URL}/{order_id}")
    return jsonify({"deleted": True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
