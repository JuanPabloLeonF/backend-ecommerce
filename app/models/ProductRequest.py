class ProductRequest():

    def __init__(self, name: str, code: str, price: str, description: str, img: str, stock: int):
        self.__name: str = name
        self.__code: str = code
        self.__price: str = price
        self.__description: str = description
        self.__img: str = img
        self.__stock: int = stock

    def getName(self) -> str:
        return self.__name

    def getCode(self) -> str:
        return self.__code

    def getPrice(self) -> str:
        return self.__price

    def getDescription(self) -> str:
        return self.__description

    def getImg(self) -> str:
        return self.__img
    
    def getStock(self) -> int:
        return self.__stock

    def setName(self, name: str):
        self.__name = name

    def setCode(self, code: str):
        self.__code = code

    def setPrice(self, price: str):
        self.__price = price

    def setDescription(self, description: str):
        self.__description = description

    def setImg(self, img: str):
        self.__img = img

    def setStock(self, stock:int):
        self.__stock = stock

    def toJSON(self) -> dict:
        return {
            'name': self.__name,
            'code': self.__code,
            'price': self.__price,
            'description': self.__description,
            'img': self.__img,
            'stock': self.__stock
        }
