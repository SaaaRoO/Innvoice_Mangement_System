from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, Unit, InvoiceDetails
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)  # Enable CORS for all routes

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    invoices = InvoiceDetails.query.all()
    return jsonify([{
        'id': inv.id,
        'lineNo': inv.lineNo,
        'productName': inv.productName,
        'unitNo': inv.unitNo,
        'price': inv.price,
        'quantity': inv.quantity,
        'total': inv.total,
        'expiryDate': inv.expiryDate.strftime('%Y-%m-%d')
    } for inv in invoices]), 200

@app.route('/api/invoices', methods=['POST'])
def add_invoice():
    data = request.get_json()
    print("Received data for new invoice:", data)  # Log received data

    # Check for existing invoice with the same lineNo
    existing_invoice = InvoiceDetails.query.filter_by(lineNo=data['lineNo']).first()
    if existing_invoice:
        print(f"Error adding invoice: Invoice with lineNo {data['lineNo']} already exists.")
        return jsonify({"error": "Invoice with this lineNo already exists."}), 400

    try:
        # Calculate total if not provided
        quantity = data.get('quantity', 0)
        price = data.get('price', 0.0)
        total = price * quantity  # Calculate total

        invoice = InvoiceDetails(
            lineNo=data['lineNo'],
            productName=data['productName'],
            unitNo=data['unitNo'],
            price=price,
            quantity=quantity,
            total=total,  # Use calculated total
            expiryDate=datetime.strptime(data['expiryDate'], '%Y-%m-%d')
        )
        db.session.add(invoice)
        db.session.commit()
        print("Invoice added successfully")  # Confirmation message
        return jsonify({"message": "Invoice added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print("Error adding invoice:", str(e))  # Error output
        return jsonify({"error": str(e)}), 500

# API to delete an invoice by id
@app.route('/api/invoices/<int:id>', methods=['DELETE'])
def delete_invoice(id):
    invoice = db.session.get(InvoiceDetails, id)  # Update here to use session.get
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    try:
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({"message": "Invoice deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print("Error deleting invoice:", str(e))
        return jsonify({"error": str(e)}), 500

# Get details of a specific invoice
@app.route('/api/invoices/<int:id>', methods=['GET'])
def get_invoice(id):
    invoice = db.session.get(InvoiceDetails, id)  # Update here to use session.get
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    return jsonify({
        'id': invoice.id,
        'lineNo': invoice.lineNo,
        'productName': invoice.productName,
        'unitNo': invoice.unitNo,
        'price': invoice.price,
        'quantity': invoice.quantity,
        'total': invoice.total,
        'expiryDate': invoice.expiryDate.strftime('%Y-%m-%d')
    }), 200

@app.route('/api/invoices/<int:id>', methods=['PUT'])
def update_invoice(id):
    data = request.get_json()
    invoice = db.session.get(InvoiceDetails, id)  # Get the invoice to update
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    # Check if the new lineNo already exists in another invoice
    new_line_no = data['lineNo']
    existing_invoice = InvoiceDetails.query.filter(
        InvoiceDetails.lineNo == new_line_no,
        InvoiceDetails.id != id  # Exclude the current invoice from the check
    ).first()

    if existing_invoice:
        return jsonify({"error": "Invoice with this lineNo already exists."}), 400

    # Update the invoice fields
    invoice.lineNo = new_line_no
    invoice.productName = data['productName']
    invoice.unitNo = data['unitNo']
    invoice.price = data['price']
    invoice.quantity = data['quantity']
    invoice.total = invoice.price * invoice.quantity  # Recalculate total
    invoice.expiryDate = datetime.strptime(data['expiryDate'], '%Y-%m-%d')

    try:
        db.session.commit()
        return jsonify({"message": "Invoice updated successfully"})
    except Exception as e:
        db.session.rollback()
        print("Error updating invoice:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
