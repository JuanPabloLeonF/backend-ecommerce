from flask import Blueprint, request

from app.repository.InvoiceRepository import InvoiceRepository

invoiceRoute = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoiceRoute.route("/create", methods=["GET"])
def create():
    return InvoiceRepository.createHtml(request.data)