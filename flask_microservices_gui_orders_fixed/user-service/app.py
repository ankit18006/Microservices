from flask import Flask, jsonify, request
app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Ankit", "email": "ankit@example.com"},
    2: {"id": 2, "name": "raja", "email": "uhwheii@gmail.com"}
}
next_id = 3

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(list(users.values()))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = users.get(user_id)
    if not u:
        return jsonify({'error':'User not found'}), 404
    return jsonify(u)

@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json() or {}
    name = data.get('name'); email = data.get('email')
    if not name or not email:
        return jsonify({'error':'name and email required'}), 400
    user = {'id': next_id, 'name': name, 'email': email}
    users[next_id] = user
    next_id += 1
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json() or {}
    u = users.get(user_id)
    if not u:
        return jsonify({'error':'User not found'}), 404
    u['name'] = data.get('name', u['name'])
    u['email'] = data.get('email', u['email'])
    return jsonify(u)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({'status':'deleted'})
    return jsonify({'error':'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
