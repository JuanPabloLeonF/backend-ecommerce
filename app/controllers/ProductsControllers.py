from werkzeug.utils import secure_filename
import os
from flask import Blueprint, jsonify, request, send_file
from app.models.ProductRequest import ProductRequest
from app.repository.ProductImgRepository import ProductImgRepository
from app.repository.ProductRepository import ProductRepository
import json
import base64
from werkzeug.datastructures import FileStorage


productRoute = Blueprint('products', __name__, url_prefix='/products')

@productRoute.route("/getAll", methods=["GET"])
def getAll():
    return ProductRepository.getAll()

@productRoute.route("/getById/<string:id>", methods=["GET"])
def getById(id:str):
    return ProductRepository.getById(id=id)

@productRoute.route("/create", methods=["POST"])
def create():

    if 'img' not in request.files:
        return jsonify({"message": "No image file found"}), 400
    
    img: FileStorage = request.files['img']

    if img.filename == '':
        return jsonify({"message": "No image file selected"}), 400

    return ProductImgRepository.saveImgAndProduct(img=img, request=request)

@productRoute.route("/updateById/<string:id>", methods=["PUT"])
def updateById(id:str):
    if 'img' not in request.files:
        return jsonify({"message": "No image file found"}), 400
    
    img = request.files['img']

    if img.filename == '':
        return jsonify({"message": "No image file selected"}), 400

    return ProductImgRepository.updateImgAndProduct(id=id, img=img, request=request)

@productRoute.route("/deleteById/<string:id>", methods=["DELETE"])
def deleteById(id:str):
    return ProductRepository.deleteById(id=id)

@productRoute.route("/deleteStock/<string:id>", methods=["PATCH"])
def deleteStock(id:str):
    stockData = json.loads(request.data)
    return ProductRepository.deleteStock(id=id, stock=stockData.get("stock"))