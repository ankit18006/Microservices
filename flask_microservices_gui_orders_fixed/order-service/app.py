from flask import Flask, jsonify, request
app = Flask(__name__)

# in-memory orders
orders = [
    {"id": 101, "user_id": 1, "item": "Laptop", "price": 75000},
    {"id": 102, "user_id": 1, "item": "Mouse", "price": 500},
    {"id": 103, "user_id": 2, "item": "Phone", "price": 25000}
]

def next_order_id():
    return max(o['id'] for o in orders) + 1 if orders else 1

@app.route('/orders', methods=['GET'])
def all_orders():
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    o = next((x for x in orders if x['id'] == order_id), None)
    if not o:
        return jsonify({'error':'Order not found'}), 404
    return jsonify(o)

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def orders_by_user(user_id):
    user_orders = [o for o in orders if o.get('user_id') == user_id]
    return jsonify(user_orders), 200

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json() or {}
    if not data or 'user_id' not in data or 'item' not in data:
        return jsonify({'error':'user_id and item required'}), 400
    new_id = next_order_id()
    order = {
        'id': new_id,
        'user_id': data['user_id'],
        'item': data['item'],
        'price': data.get('price', 0)
    }
    orders.append(order)
    return jsonify(order), 201

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    idx = next((i for i,o in enumerate(orders) if o['id']==order_id), None)
    if idx is None:
        return jsonify({'error':'Order not found'}), 404
    orders.pop(idx)
    return jsonify({'status':'deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
