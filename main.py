from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()

class ProductCreateModel(BaseModel):
    name: str = Field(...)
    price: float = Field(...)
    amount: int = Field(...)

    model_config = ConfigDict(
        json_schema_extra = {
            'example': {
                "name": "Apple",
                "price": 1234,
                "amount": 2345
            }
        }
    )

class ProductUpdateModel(BaseModel):
    name: str = Field(...)
    price: float = Field(...)
    amount: int = Field(...)

    model_config = ConfigDict(
        json_schema_extra = {
            'example': {
                "name": "Banana",
                "price": 12,
                "amount": 1234
            }
        }
    )

products = []
@app.get('/product')
def get_all_product():
    return products

@app.post('/product')
def create_product(product: ProductCreateModel = Body()):
    product_dict = {
        'id': len(products) + 1,
        'name': product.name,
        'price': product.price,
        'amount': product.amount
    }

    products.append(product_dict)

    return {'message': 'Create product successfully.'}

@app.get('/product/{id}')
def get_product_by_id(id: int):
    product = None

    for item in products:
        if id == item['id']:
            product = item

    if not product:
        return {'message': 'Product not found.'}
    
    return product

@app.put('/product/{id}')
def update_product_by_id(id: int,
                         product_update: ProductUpdateModel = Body()):
    product = None
    product_idx = 0

    for idx, item in enumerate(products):
        if id == item['id']:
            product = item
            product_idx = idx

        if not product:
            return {'message': 'Product not found.'}
    
    products[product_idx]['name'] = product_update.name
    products[product_idx]['price'] = product_update.price
    products[product_idx]['amount'] = product_update.amount

    return {'message': 'Update successfully.'}

@app.delete('/product/{id}')
def delete_product_by_id(id: int):
    product = None

    for item in products:
        if id == item['id']:
            product = item
        
    if not product:
        return {'message': 'Product not found.'}
    
    product_temp = []
    for item in products:
        if id != item['id']:
            product_temp.append(item)
    
    products = product_temp

    return {'message': 'Delete successfully.'}




'''
{
"name" : "Apple",
"price": 15,
"amount": 100
}
'''