from flask import Flask, render_template, request, redirect

from flask_mail import Mail, Message

from blockchain import Blockchain

from database import (
    create_table,
    insert_invoice,
    get_all_invoices,
    update_invoice_status
)

app = Flask(__name__)

# -----------------------------
# EMAIL CONFIGURATION
# -----------------------------

app.config['MAIL_SERVER'] = 'smtp.gmail.com'

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'vermaharshita2601@gmail.com'

app.config['MAIL_PASSWORD'] = 'Harshita@2601'

mail = Mail(app)

# -----------------------------
# BLOCKCHAIN
# -----------------------------

blockchain = Blockchain()

create_table()

# -----------------------------
# HOME DASHBOARD
# -----------------------------

@app.route('/')
def home():

    chain = blockchain.display_chain()

    invoices = get_all_invoices()

    # SEARCH
    search = request.args.get('search', '')

    # FILTER
    status_filter = request.args.get('status', '')

    # SEARCH BY COMPANY
    if search:

        chain = [
            block for block in chain
            if isinstance(block["Data"], dict)
            and search.lower() in block["Data"]["company"].lower()
        ]

    # FILTER BY STATUS
    if status_filter:

        chain = [
            block for block in chain
            if isinstance(block["Data"], dict)
            and block["Data"]["status"] == status_filter
        ]

    # DASHBOARD COUNTS

    total = len(invoices)

    approved = len([
        invoice for invoice in invoices
        if invoice[5] == "Approved"
    ])

    rejected = len([
        invoice for invoice in invoices
        if invoice[5] == "Rejected"
    ])

    pending = len([
        invoice for invoice in invoices
        if invoice[5] == "Pending"
    ])

    return render_template(
        'dashboard.html',
        chain=chain,
        invoices=invoices,
        total=total,
        approved=approved,
        rejected=rejected,
        pending=pending
    )

# -----------------------------
# UPLOAD INVOICE
# -----------------------------

@app.route('/upload', methods=['GET', 'POST'])
def upload_invoice():

    if request.method == 'POST':

        invoice_id = request.form['invoice_id']

        company = request.form['company']

        amount = request.form['amount']

        buyer = request.form['buyer']

        email = request.form['email']

        invoice_data = {
            "invoice_id": invoice_id,
            "company": company,
            "amount": amount,
            "buyer": buyer,
            "email": email,
            "status": "Pending"
        }

        # ADD TO BLOCKCHAIN
        blockchain.add_block(invoice_data)

        # ADD TO DATABASE
        insert_invoice(
            invoice_id,
            company,
            amount,
            buyer,
            "Pending"
        )

        return redirect('/')

    return render_template('upload.html')

# -----------------------------
# APPROVE INVOICE
# -----------------------------

@app.route('/approve/<int:block_id>')
def approve_invoice(block_id):

    # UPDATE BLOCKCHAIN
    blockchain.update_status(block_id, "Approved")

    block = blockchain.chain[block_id]

    invoice_id = block.data['invoice_id']

    # UPDATE DATABASE
    update_invoice_status(invoice_id, "Approved")

    # CLIENT EMAIL
    receiver = block.data['email']

    # EMAIL MESSAGE
    msg = Message(
        'Invoice Approved',
        sender=app.config['MAIL_USERNAME'],
        recipients=[receiver]
    )

    msg.body = f"""
            Hello,

            Congratulations!

            Your invoice has been APPROVED.

            Invoice ID: {block.data['invoice_id']}

            Company: {block.data['company']}

            Amount: ₹{block.data['amount']}

            The invoice is now verified in the TReDS Blockchain System.

            Thank you.
            """

    # SEND EMAIL
    mail.send(msg)

    return redirect('/')

# -----------------------------
# REJECT INVOICE + EMAIL ALERT
# -----------------------------

@app.route('/reject/<int:block_id>')
def reject_invoice(block_id):

    # UPDATE BLOCKCHAIN
    blockchain.update_status(block_id, "Rejected")

    block = blockchain.chain[block_id]

    invoice_id = block.data['invoice_id']

    # UPDATE DATABASE
    update_invoice_status(invoice_id, "Rejected")

    # GET CLIENT EMAIL
    receiver = block.data['email']

    # EMAIL MESSAGE
    msg = Message(
        'Invoice Rejected',
        sender=app.config['MAIL_USERNAME'],
        recipients=[receiver]
    )

    msg.body = f"""
Hello,

Your invoice has been REJECTED.

Invoice ID: {block.data['invoice_id']}

Company: {block.data['company']}

Amount: ₹{block.data['amount']}

Please contact support for further clarification.

TReDS Blockchain System
"""

    # SEND EMAIL
    mail.send(msg)

    return redirect('/')

# -----------------------------
# RUN APP
# -----------------------------

if __name__ == '__main__':

    app.run(debug=True)