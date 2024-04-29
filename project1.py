from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# Create Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

# Define Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, nullable=False, default=0)

# Define Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)

# Create database tables
db.create_all()

# Endpoint to add a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.json
        new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer added successfully'}), 201
    except KeyError:
        return jsonify({'message': 'Invalid data format'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

# Endpoint to retrieve customer details
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number})
    else:
        return jsonify({'message': 'Customer not found'}), 404

# Endpoint to update customer details
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.json
        customer = Customer.query.get(customer_id)
        if customer:
            customer.name = data.get('name', customer.name)
            customer.email = data.get('email', customer.email)
            customer.phone_number = data.get('phone_number', customer.phone_number)
            db.session.commit()
            return jsonify({'message': 'Customer updated successfully'}), 200
        else:
            return jsonify({'message': 'Customer not found'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

# Endpoint to delete a customer
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404

# Endpoint to add a new product
@app.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.json
        new_product = Product(name=data['name'], price=data['price'], stock_level=data.get('stock_level', 0))
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except KeyError:
        return jsonify({'message': 'Invalid data format'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

# Endpoint to retrieve product details
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'stock_level': product.stock_level})
    else:
        return jsonify({'message': 'Product not found'}), 404

# Endpoint to update product details
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.json
        product = Product.query.get(product_id)
        if product:
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.stock_level = data.get('stock_level', product.stock_level)
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

# Endpoint to delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

# Endpoint to place a new order
@app.route('/orders', methods=['POST'])
def place_order():
    try:
        data = request.json
        new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'],
                          quantity=data['quantity'], order_date=data['order_date'])
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order placed successfully'}), 201
    except KeyError:
        return jsonify({'message': 'Invalid data format'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

# Main function to run the application
if __name__ == '__main__':
    app.run(debug=True)
