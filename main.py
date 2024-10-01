import os
from flask import Flask
from app.configuration.configuration import db, init_app
from app.controllers.ProductsControllers import productRoute
from app.controllers.InvoiceController import invoiceRoute

app = Flask(__name__)
init_app(app)
app.register_blueprint(productRoute)
app.register_blueprint(invoiceRoute)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
    with app.app_context():
        db.create_all()