import uvicorn
from fastapi import FastAPI
from orders.repositories.order import OrderRepository
from orders.repositories.product import ProductRepository
from orders.database.database import Database
from orders.models.order import Order
from orders.models.product import Product
from orders.services.order import OrderService
from orders.services.product import ProductService
from typing import List

app = FastAPI()
product_repository = ProductRepository()
order_repository = OrderRepository(product_repository)
order_service = OrderService(order_repository)
product_service = ProductService(product_repository)
_ = Database()


@app.get('/api/products', response_model=List[Product])
async def retrieve_products():
    return product_service.get_all()


@app.get('/api/products/{product_number}')
async def retrieve_product_by_number(product_number):
    product = product_service.get_one(product_number)
    if product:
        return product
    else:
        return {}


@app.post('/api/orders/new')
async def create_order(order: Order):
    order.total = round(order.quantity * order.product.unit_cost, 2)
    return order_service.add_new(order)


@app.get('/api/orders/{order_number}')
async def retrieve_order_by_number(order_number):
    order = order_service.get_one(order_number)
    if order:
        return order
    else:
        return {}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True,
                timeout_keep_alive=3600, debug=True, workers=10)
