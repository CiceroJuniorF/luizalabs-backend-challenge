
from src.domain.entities.favorite_product import FavoriteProduct
from src.domain.errors.domain_error import DomainError


ID = "1234AA"
PRODUCT_ID = "1234BB"
CUSTOMER_ID = "1234CC"
TITLE_PRODUCT = "Product"
IMAGE_PRODUCT = "https/luiza.com/image.jpg"
PRICE_PRODUCT = 10.0


def test_should_create_favorite_product():
    favorite_product = FavoriteProduct(id=ID, 
                                       customer_id=CUSTOMER_ID, 
                                       product_id=PRODUCT_ID, 
                                       title=TITLE_PRODUCT, 
                                       image=IMAGE_PRODUCT, 
                                       price=PRICE_PRODUCT)
    assert favorite_product.id == ID 
    assert favorite_product.customer_id == CUSTOMER_ID
    assert favorite_product.product_id == PRODUCT_ID
    assert favorite_product.title == TITLE_PRODUCT
    assert favorite_product.image == IMAGE_PRODUCT
    assert favorite_product.price == PRICE_PRODUCT

def test_shouldnt_create_favorite_product_with_all_fields_empty():
    try:
        FavoriteProduct(id="", customer_id="", product_id="", title="", image="", price=0)
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Id is required, Customer id is required, Product id is required, Title is required, Image is required, Price is required"

def test_should_create_favorite_product_from_dict():
    favorite_product = FavoriteProduct.from_dict({"id":ID, 
                                                  "customer_id":CUSTOMER_ID, 
                                                  "product_id":PRODUCT_ID, 
                                                  "title":TITLE_PRODUCT, 
                                                  "image":IMAGE_PRODUCT, 
                                                  "price":PRICE_PRODUCT})
    assert favorite_product.id == ID
    assert favorite_product.customer_id == CUSTOMER_ID  
    assert favorite_product.product_id == PRODUCT_ID
    assert favorite_product.title == TITLE_PRODUCT
    assert favorite_product.image == IMAGE_PRODUCT
    assert favorite_product.price == PRICE_PRODUCT

def test_shouldnt_create_favorite_product_from_dict_with_all_fields_empty():
    try:
        FavoriteProduct.from_dict({"id":"", 
                                   "customer_id":"", 
                                   "product_id":"", 
                                   "title":"", 
                                   "image":"", 
                                   "price":0})
    except Exception as e:
        assert isinstance(e, DomainError)
        assert str(e) == "Id is required, Customer id is required, Product id is required, Title is required, Image is required, Price is required"

def test_should_return_dict():
    favorite_product = FavoriteProduct(id=ID, 
                                       customer_id=CUSTOMER_ID, 
                                       product_id=PRODUCT_ID, 
                                       title=TITLE_PRODUCT, 
                                       image=IMAGE_PRODUCT, 
                                       price=PRICE_PRODUCT)
    assert favorite_product.to_dict() == {"id":ID, 
                                          "customer_id":CUSTOMER_ID, 
                                          "product_id":PRODUCT_ID, 
                                          "title":TITLE_PRODUCT, 
                                          "image":IMAGE_PRODUCT, 
                                          "price":PRICE_PRODUCT
                                        }