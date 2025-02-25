from src.domain.interfaces.gateway.product_service import ProductOutput, ProductService


class ProductServiceMemory(ProductService): 
    def __init__(self):
        self.products = [
            ProductOutput.from_dict({
                "id": "51150cf9-2f86-4bc9-bd71-4cfccca5d111",
                "title": "Product 1",
                "image": "https://luizalabs.com/api/images/1",
                "price": 10.0
            }),
            ProductOutput.from_dict({
                "id": "85aafccb-44bf-4bff-b66c-f9581eb96742",
                "title": "Product 2",
                "image": "https://luizalabs.com/api/images/2",
                "price": 20.0
            }),
            ProductOutput.from_dict({
                "id": "8a9a59b9-5c8e-4dc4-8260-ac4a3699bccc",
                "title": "Product 3",
                "image": "https://luizalabs.com/api/images/3",
                "price": 30.0
            }),
        ]



    def get(self, product_id: str) -> ProductOutput:
        products = list(filter(lambda product: product.id == product_id, self.products))
        return products[0] if products else None
