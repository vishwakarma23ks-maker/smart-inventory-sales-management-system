"""
Smart Inventory & Sales Management System (SmartStock)
Backend Entry Point: app.py
Framework: Flask 3.0+ / SQLAlchemy / Jinja2
Designed for Academic Submission & Production Deployment
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'smartstock.db')
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'smartstock_secret_key_2026')
# Prefer a local SQLite database by default so the project runs without a MySQL server.
# If DATABASE_URL is set explicitly, it will override this default.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    f'sqlite:///{DB_PATH}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# DATABASE MODELS
# ==========================================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship('Product', backref='category', lazy=True)

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    products = db.relationship('Product', backref='supplier', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)  # Simple name: Mouse, Keyboard, Cable, etc.
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    purchase_price = db.Column(db.Float, default=0.0)
    selling_price = db.Column(db.Float, default=0.0)
    stock_quantity = db.Column(db.Integer, default=0)
    minimum_stock = db.Column(db.Integer, default=10)
    status = db.Column(db.String(30), default='In Stock')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Krishna, Golam, Babli
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    total_purchases = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    sales = db.relationship('Sale', backref='customer', lazy=True)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(40), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    subtotal = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    tax = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(30), default='UPI')
    status = db.Column(db.String(20), default='Paid')
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref='sales', lazy=True)


class InventoryRecord(db.Model):
    __tablename__ = 'inventory_records'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='inventory_records', lazy=True)
    movement_type = db.Column(db.String(20), nullable=False, default='stock_in')
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, default=0.0)
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==========================================
# SEED INITIAL DATA
# ==========================================
def migrate_columns():
    """Add columns that may be missing from an existing SQLite database."""
    with app.app_context():
        db.create_all()
        # SQLite-only migration helper; MySQL schemas are provisioned via database.sql.
        if 'sqlite' not in app.config['SQLALCHEMY_DATABASE_URI']:
            return
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        existing = {row[1] for row in cursor.execute("PRAGMA table_info(sales)").fetchall()}
        if 'product_id' not in existing:
            cursor.execute("ALTER TABLE sales ADD COLUMN product_id INTEGER REFERENCES products(id)")
        if 'quantity' not in existing:
            cursor.execute("ALTER TABLE sales ADD COLUMN quantity INTEGER DEFAULT 1")
        conn.commit()
        conn.close()


def seed_data():
    with app.app_context():
        migrate_columns()
        if not User.query.first():
            admin = User(
                name='Krishna',
                email='krishna@smartstock.in',
                password_hash=generate_password_hash('Admin@123'),
                role='admin'
            )
            db.session.add(admin)

        if not Customer.query.first():
            c1 = Customer(name='Krishna', phone='+91 98111 22334', email='krishna@example.com')
            c2 = Customer(name='Golam', phone='+91 98222 33445', email='golam@example.com')
            c3 = Customer(name='Babli', phone='+91 98333 44556', email='babli@example.com')
            db.session.add_all([c1, c2, c3])

        if not Category.query.first():
            cat1 = Category(name='Accessories', description='Workstation and computer gear')
            cat2 = Category(name='Cables', description='Connectivity and fast charging')
            cat3 = Category(name='Audio', description='Speakers and audio gear')
            db.session.add_all([cat1, cat2, cat3])
            db.session.commit()

            # Simple product names
            p1 = Product(name='Mouse', category_id=cat1.id, purchase_price=480, selling_price=799, stock_quantity=4, minimum_stock=10, status='Low Stock')
            p2 = Product(name='Keyboard', category_id=cat1.id, purchase_price=1650, selling_price=2899, stock_quantity=42, minimum_stock=10, status='In Stock')
            p3 = Product(name='Cable', category_id=cat2.id, purchase_price=190, selling_price=349, stock_quantity=6, minimum_stock=15, status='Low Stock')
            p4 = Product(name='Stand', category_id=cat1.id, purchase_price=650, selling_price=1199, stock_quantity=3, minimum_stock=10, status='Low Stock')
            p5 = Product(name='Speaker', category_id=cat3.id, purchase_price=1450, selling_price=2499, stock_quantity=5, minimum_stock=12, status='Low Stock')
            p6 = Product(name='Printer', category_id=cat1.id, purchase_price=3800, selling_price=5699, stock_quantity=14, minimum_stock=5, status='In Stock')
            p7 = Product(name='Scanner', category_id=cat1.id, purchase_price=1100, selling_price=1899, stock_quantity=28, minimum_stock=8, status='In Stock')
            db.session.add_all([p1, p2, p3, p4, p5, p6, p7])
            db.session.commit()


def update_product_status(product):
    if product.stock_quantity <= 0:
        product.status = 'Out of Stock'
    elif product.stock_quantity <= product.minimum_stock:
        product.status = 'Low Stock'
    else:
        product.status = 'In Stock'


def get_dashboard_context():
    products = Product.query.order_by(Product.id.asc()).all()
    customers = Customer.query.order_by(Customer.id.asc()).all()
    sales = Sale.query.order_by(Sale.sale_date.desc()).all()
    inventory_logs = InventoryRecord.query.order_by(InventoryRecord.created_at.desc()).limit(8).all()
    total_stock = sum(p.stock_quantity for p in products)
    low_stock = [p for p in products if p.stock_quantity <= p.minimum_stock]
    return {
        'products': products,
        'customers': customers,
        'sales': sales,
        'inventory_logs': inventory_logs,
        'total_stock': total_stock,
        'low_stock': low_stock,
        'user_name': session.get('user_name', 'Krishna')
    }

# ==========================================
# APPLICATION ROUTES
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_product':
            name = request.form.get('name', '').strip()
            category_name = request.form.get('category', '').strip()
            supplier_name = request.form.get('supplier', '').strip()
            purchase_price = float(request.form.get('purchase_price', 0) or 0)
            selling_price = float(request.form.get('selling_price', 0) or 0)
            stock_quantity = int(request.form.get('stock_quantity', 0) or 0)
            minimum_stock = int(request.form.get('minimum_stock', 0) or 0)

            if not name or not category_name:
                flash('Product name and category are required.', 'error')
                return redirect(url_for('dashboard'))

            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name, description='Added from dashboard')
                db.session.add(category)
                db.session.commit()

            supplier = None
            if supplier_name:
                supplier = Supplier.query.filter_by(name=supplier_name).first()
                if not supplier:
                    supplier = Supplier(
                        name=supplier_name,
                        company='Local Supplier',
                        phone='0000000000',
                        email=''
                    )
                    db.session.add(supplier)
                    db.session.commit()

            product = Product(
                name=name,
                category_id=category.id,
                supplier_id=supplier.id if supplier else None,
                purchase_price=purchase_price,
                selling_price=selling_price,
                stock_quantity=stock_quantity,
                minimum_stock=minimum_stock,
            )
            update_product_status(product)
            db.session.add(product)
            db.session.commit()

            inventory_record = InventoryRecord(
                product_id=product.id,
                movement_type='stock_in',
                quantity=stock_quantity,
                unit_price=purchase_price,
                note='New product added via dashboard'
            )
            db.session.add(inventory_record)
            db.session.commit()
            flash(f'Product {name} added successfully.', 'success')

        elif action == 'update_stock':
            product_id = request.form.get('product_id', type=int)
            movement_type = request.form.get('movement_type', 'stock_in')
            quantity = int(request.form.get('quantity', 0) or 0)
            note = request.form.get('note', '').strip() or 'Stock updated from dashboard'

            if not product_id or quantity <= 0:
                flash('Please select a product and valid quantity.', 'error')
                return redirect(url_for('dashboard'))

            product = Product.query.get_or_404(product_id)
            if movement_type == 'stock_out':
                if quantity > product.stock_quantity:
                    flash(f'Not enough stock for {product.name}. Available: {product.stock_quantity}', 'error')
                    return redirect(url_for('dashboard'))
                product.stock_quantity -= quantity
            else:
                product.stock_quantity += quantity

            update_product_status(product)
            inventory_record = InventoryRecord(
                product_id=product.id,
                movement_type=movement_type,
                quantity=quantity,
                unit_price=product.purchase_price,
                note=note
            )
            db.session.add(inventory_record)
            db.session.commit()
            flash(f'Stock updated for {product.name}.', 'success')

        return redirect(url_for('dashboard'))

    context = get_dashboard_context()
    context['sales'] = Sale.query.order_by(Sale.sale_date.desc()).all()
    return render_template('dashboard.html', **context)


@app.route('/dashboard/customer', methods=['POST'])
def add_customer():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    address = request.form.get('address', '').strip()

    if not name or not phone:
        flash('Customer name and phone are required.', 'error')
        return redirect(url_for('dashboard'))

    existing = Customer.query.filter_by(phone=phone).first()
    if existing:
        flash(f'A customer with phone {phone} already exists.', 'error')
        return redirect(url_for('dashboard'))

    customer = Customer(
        name=name,
        phone=phone,
        email=email or None,
        address=address or None,
    )
    db.session.add(customer)
    db.session.commit()
    flash(f'Customer {name} added successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/dashboard/sale', methods=['POST'])
def record_sale():
    product_id = request.form.get('product_id', type=int)
    customer_id = request.form.get('customer_id', type=int)
    qty = int(request.form.get('quantity', 0) or 0)
    payment_method = request.form.get('payment_method', 'UPI').strip() or 'UPI'
    note = request.form.get('note', '').strip()

    product = Product.query.get(product_id)
    customer = Customer.query.get(customer_id)

    if not product:
        flash('Please select a valid product.', 'error')
        return redirect(url_for('dashboard'))
    if not customer:
        flash('Please select a customer.', 'error')
        return redirect(url_for('dashboard'))
    if qty <= 0:
        flash('Quantity must be greater than zero.', 'error')
        return redirect(url_for('dashboard'))
    if product.stock_quantity < qty:
        flash(f'Not enough stock for {product.name}. Available: {product.stock_quantity}', 'error')
        return redirect(url_for('dashboard'))

    # Auto deduct inventory
    product.stock_quantity -= qty
    update_product_status(product)

    subtotal = product.selling_price * qty
    tax = round(subtotal * 0.18, 2)
    total = round(subtotal + tax, 2)

    sale = Sale(
        invoice_number=f"INV-{1000 + Sale.query.count() + 1}",
        customer_id=customer.id,
        product_id=product.id,
        quantity=qty,
        subtotal=subtotal,
        discount=0.0,
        tax=tax,
        total_amount=total,
        payment_method=payment_method,
        status='Paid'
    )
    db.session.add(sale)
    db.session.commit()

    customer.total_purchases += 1
    customer.total_spent += total
    db.session.commit()

    db.session.add(InventoryRecord(
        product_id=product.id,
        movement_type='stock_out',
        quantity=qty,
        unit_price=product.selling_price,
        note=note or f'Sold to {customer.name} via {payment_method}'
    ))
    db.session.commit()

    flash(f'Sale recorded! Invoice {sale.invoice_number} — ₹{total} for {qty}x {product.name}.', 'success')
    return redirect(url_for('dashboard'))

# ==========================================
# REST API (JSON ENDPOINTS)
# ==========================================

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'category': p.category.name if p.category else 'General',
        'selling_price': p.selling_price,
        'stock_quantity': p.stock_quantity,
        'status': p.status
    } for p in products])

@app.route('/api/sales', methods=['POST'])
def create_sale():
    data = request.json
    customer = Customer.query.get(data.get('customer_id'))
    product = Product.query.get(data.get('product_id'))
    qty = int(data.get('quantity', 1))

    if not product or product.stock_quantity < qty:
        return jsonify({'error': 'Insufficient stock'}), 400

    # Auto deduct inventory
    product.stock_quantity -= qty
    if product.stock_quantity == 0:
        product.status = 'Out of Stock'
    elif product.stock_quantity <= product.minimum_stock:
        product.status = 'Low Stock'

    subtotal = product.selling_price * qty
    tax = subtotal * 0.18
    total = subtotal + tax

    sale = Sale(
        invoice_number=f"INV-{1000 + Sale.query.count() + 1}",
        customer_id=customer.id if customer else 1,
        product_id=product.id,
        quantity=qty,
        subtotal=subtotal,
        tax=tax,
        total_amount=total,
        payment_method=data.get('payment_method', 'UPI')
    )
    db.session.add(sale)
    db.session.commit()

    return jsonify({'success': True, 'invoice_number': sale.invoice_number, 'total': total})

if __name__ == '__main__':
    seed_data()
    app.run(debug=True, port=5000)
