import os
from app.models.ProductRequest import ProductRequest
import base64
from flask import jsonify, Request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

class ProductImgRepository:

    UPLOAD_FOLDER = 'app/assets/imgs'

    @staticmethod
    def allowedFile(filename: str):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def getImgBase64(imgUrl: str):
        with open(imgUrl, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    @staticmethod
    def saveImgAndProduct(img: FileStorage, request: Request):
        from app.repository.ProductRepository import ProductRepository
        if ProductImgRepository.allowedFile(img.filename):
            filename = secure_filename(img.filename)
            imgPath = os.path.join(ProductImgRepository.UPLOAD_FOLDER, filename)
            img.save(imgPath)

            productRequest = ProductRequest(
                name=request.form['name'],
                code=request.form['code'],
                description=request.form['description'],
                price=request.form['price'],
                img=imgPath,
                stock=request.form['stock']
            )

            response, statusCode = ProductRepository.create(productRequest=productRequest)
            
            if statusCode == 201:
                productData = response.get_json()
                imgUrl = productData.get('img')
                imgBase64 = ProductImgRepository.getImgBase64(imgUrl=imgUrl)

                return jsonify({
                    "product": productData,
                    "image": imgBase64
                }), 201

            elif statusCode in [400, 500]:
                return jsonify(response.get_json()), statusCode

        return jsonify({"message": "Invalid image file format"}), 400

    @staticmethod
    def updateImgAndProduct(id: str, img: FileStorage, request: Request):
        from app.repository.ProductRepository import ProductRepository  

        existing_product, status_code = ProductRepository.getById(id=id)
        if status_code == 404:
            return jsonify({"message": "Product not found"}), 404

        existing_product_data = existing_product.get_json()

        if img and ProductImgRepository.allowedFile(img.filename):
            if existing_product_data.get('img'):
                old_img_path = existing_product_data['img']
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)

            filename = secure_filename(img.filename)
            imgPath = os.path.join(ProductImgRepository.UPLOAD_FOLDER, filename)
            img.save(imgPath)
        else:
            imgPath = existing_product_data.get('img')

        productRequest = ProductRequest(
            name=request.form.get('name', existing_product_data.get('name')),
            code=request.form.get('code', existing_product_data.get('code')),
            description=request.form.get('description', existing_product_data.get('description')),
            price=request.form.get('price', existing_product_data.get('price')),
            img=imgPath,
            stock=request.form.get('stock', existing_product_data.get('stock'))
        )

        response, statusCode = ProductRepository.updateById(id=id, productRequest=productRequest)

        if statusCode == 200:
            productData = response.get_json()
            imgBase64 = ProductImgRepository.getImgBase64(imgUrl=imgPath)

            return jsonify({
                "product": productData,
                "image": imgBase64
            }), 200

        return jsonify(response.get_json()), statusCode

    @staticmethod
    def deleteImg(imgUrl: str):
        if os.path.exists(imgUrl):
            os.remove(imgUrl)

