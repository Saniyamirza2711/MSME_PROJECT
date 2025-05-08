from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get_inventory', methods=['GET'])
def get_inventory():
    return jsonify({"message": "Inventory fetched successfully"})

if __name__ == '__main__':
    app.run(debug=True)