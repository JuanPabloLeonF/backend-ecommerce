from sqlite3 import IntegrityError
from app.entities.ProductEntity import ProductEntity
from app.configuration.configuration import db
from flask import jsonify
from app.models.ProductRequest import ProductRequest
from app.repository.ProductImgRepository import ProductImgRepository
import json

class ProductRepository:

    @classmethod
    def getAll(ctr):
        productsEntity: list[ProductEntity] = ProductEntity.query.all()
        productsList: list[dict] = [ product.mapperToJSON() for product in productsEntity]
        producdsResponse: list[dict] = []
        for product in productsList:
            product['img'] = ProductImgRepository.getImgBase64(imgUrl=product.get('img'))
            producdsResponse.append(product)
        return jsonify(producdsResponse), 200
    
    @classmethod
    def getById(ctr, id:str):
        try:
            productEntity: ProductEntity = ProductEntity.query.get(id)

            if not productEntity:
                raise ValueError(f"El producto no fue encontrado con el id: {id}") 

            productResponse = productEntity.mapperToJSON()
            productResponse['img'] = ProductImgRepository.getImgBase64(imgUrl=productResponse.get('img'))
            
            return jsonify(productResponse), 201
        
        except ValueError as error:
            return  jsonify(
                {
                    "statusCode": 404,
                    "status": "NOT FOUND",
                    "message": str(error),
                }
            ), 404
        
        except Exception as error:
            return  jsonify(
                {
                    "message": str(error),
                }
            ), 500   

    @classmethod
    def create(ctr, productRequest: ProductRequest):
        try:
            productEntity: ProductEntity = ProductEntity(
                name=productRequest.getName(),
                code=productRequest.getCode(),
                price=productRequest.getPrice(),
                description=productRequest.getDescription(),
                img=productRequest.getImg(),
                stock=productRequest.getStock()
            )

            db.session.add(productEntity)
            db.session.commit()

            return jsonify(productEntity.mapperToJSON()), 201
        
        except IntegrityError as e:
            db.session.rollback()
            return jsonify(
                {
                    "status": "BAD REQUEST",
                    "statusCode": 400,
                    "message": "Product already exists"
                }
            ), 400
        
        except Exception as error:
            return  jsonify(
                {
                    "message": str(error),
                }
            ), 500 

    @classmethod
    def updateById(ctr, productRequest: ProductRequest, id:str):
        try:
            productEntity: ProductEntity = ProductEntity.query.get(id)

            if productEntity:
                productEntity.name = productRequest.getName()
                productEntity.price = productRequest.getPrice()
                productEntity.code = productRequest.getCode()
                productEntity.img = productRequest.getImg()
                productEntity.description = productRequest.getDescription()
                productEntity.stock = productRequest.getStock()
                db.session.commit()
                return jsonify(productEntity.mapperToJSON()), 200
            else:
                raise ValueError(f"El producto con el id {id}, no existe")

        except ValueError as e:
            db.session.rollback()
            return jsonify(
                {
                    "status": "NOT FOUND",
                    "statusCode": 404,
                    "message": str(e)
                }
            ), 400

        except IntegrityError as e:
            db.session.rollback()
            return jsonify(
                    {
                        "status": "BAD REQUEST",
                        "statusCode": 404,
                        "message": str(e)
                    }
                ), 400
        
        except Exception as error:
            db.session.rollback()
            return  jsonify(
                {
                    "message": str(error),
                }
            ), 500 

    @classmethod
    def deleteById(ctr, id:str):
        try:
            productEntity: ProductEntity = ProductEntity.query.get(id)
            if productEntity:

                if productEntity.img:
                    ProductImgRepository.deleteImg(imgUrl=productEntity.img)

                db.session.delete(productEntity)
                db.session.commit()
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                raise ValueError(f"El producto con el id {id}, no existe")
            
        except ValueError as e:
            db.session.rollback()
            return jsonify(
                {
                    "status": "NOT FOUND",
                    "statusCode": 404,
                    "message": str(e)
                }
            ), 400
        
        except Exception as error:
            db.session.rollback()
            return  jsonify(
                {
                    "message": str(error),
                }
            ), 500 

    @classmethod
    def deleteStock(ctr, id:str, stock:int):
        try:
            productEntity: ProductEntity = ProductEntity.query.get(id)

            if productEntity:
                stockTotal: int = productEntity.stock - stock
                productEntity.stock = stockTotal
                db.session.commit()
                return jsonify(productEntity.mapperToJSON()), 200
            else:
                raise ValueError(f"El producto con el id {id}, no existe")

        except ValueError as e:
            db.session.rollback()
            return jsonify(
                {
                    "status": "NOT FOUND",
                    "statusCode": 404,
                    "message": str(e)
                }
            ), 400

        except IntegrityError as e:
            db.session.rollback()
            return jsonify(
                    {
                        "status": "BAD REQUEST",
                        "statusCode": 404,
                        "message": str(e)
                    }
                ), 400
        
        except Exception as error:
            db.session.rollback()
            return  jsonify(
                {
                    "message": str(error),
                }
            ), 500 