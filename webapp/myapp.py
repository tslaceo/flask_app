from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Update with your password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:Dota2fans@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify(product.serialize())
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.serialize()), 201

@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if product:
        data = request.get_json()
        product.name = data['name']
        product.price = data['price']
        product.quantity = data['quantity']
        db.session.commit()
        return jsonify(product.serialize())
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    else:
        return jsonify({'error': 'Product not found'}), 404

# Helper method to serialize data
def serialize(self):
    return {
        'id': self.id,
        'name': self.name,
        'price': self.price,
        'quantity': self.quantity
    }

# Attach the serialize method to the Product class
setattr(Product, "serialize", serialize)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
