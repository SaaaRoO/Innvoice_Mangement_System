// URL to the Flask API (update to your Flask API's actual URL)
const API_URL = 'http://localhost:5000/api/invoices';

// Fetch and display all invoices
async function fetchInvoices() {
    const response = await fetch(API_URL);
    const invoices = await response.json();
    const invoiceTable = document.getElementById('invoiceTable');
    invoiceTable.innerHTML = '';
    invoices.forEach(invoice => {
        invoiceTable.innerHTML += `
            <tr>
                <td>${invoice.lineNo}</td>
                <td>${invoice.productName}</td>
                <td>${invoice.unitNo}</td>
                <td>${invoice.price}</td>
                <td>${invoice.quantity}</td>
                <td>${invoice.total}</td>
                <td>${invoice.expiryDate}</td>
                <td>
                    <button class="edit-button" data-invoice-id="${invoice.id}">Edit</button>
                    <button onclick="deleteInvoice(${invoice.id})">Delete</button>
                </td>
            </tr>`;
    });
}

// Add a new invoice
document.getElementById('addInvoiceForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = {
        lineNo: document.getElementById('lineNo').value,
        productName: document.getElementById('productName').value,
        unitNo: document.getElementById('unitNo').value,
        price: parseFloat(document.getElementById('price').value),
        quantity: parseInt(document.getElementById('quantity').value),
        expiryDate: document.getElementById('expiryDate').value
    };
    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    fetchInvoices(); // Refresh the list
});

// Delete an invoice
async function deleteInvoice(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    fetchInvoices();
}

// Edit an invoice
async function editInvoice(id) {
    // Load the current data into the form
    const response = await fetch(`${API_URL}/${id}`);
    const invoice = await response.json();

    document.getElementById('lineNo').value = invoice.lineNo;
    document.getElementById('productName').value = invoice.productName;
    document.getElementById('unitNo').value = invoice.unitNo;
    document.getElementById('price').value = invoice.price;
    document.getElementById('quantity').value = invoice.quantity;
    document.getElementById('expiryDate').value = invoice.expiryDate;

    // Set the ID of the invoice to be updated
    document.getElementById('editInvoiceId').value = id;

    // Set up the form submission for the updated invoice
    document.getElementById('addInvoiceForm').onsubmit = async (event) => {
        event.preventDefault();

        const updatedInvoice = {
            lineNo: document.getElementById('lineNo').value,
            productName: document.getElementById('productName').value,
            unitNo: document.getElementById('unitNo').value,
            price: parseFloat(document.getElementById('price').value),
            quantity: parseInt(document.getElementById('quantity').value),
            expiryDate: document.getElementById('expiryDate').value
        };

        // Send a PUT request to update the invoice
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedInvoice)
        });

        if (response.ok) {
            console.log('Invoice updated successfully');
            fetchInvoices(); // Refresh the list
        } else {
            console.error('Failed to update invoice');
        }
    };
}

// Load existing invoice data into the edit form when the edit button is clicked
document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', function() {
        const invoiceId = this.dataset.invoiceId; // Get the invoice ID from a data attribute
        editInvoice(invoiceId);
    });
});

// Initial fetch to display invoices when the page loads
fetchInvoices();
