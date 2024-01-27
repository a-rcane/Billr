from flask import request
from base.db_ops.product_ops import ProductOperations
from models.product import Product

product = ProductOperations()


def add_product_info():
    try:
        product_name = request.args.get('product_name')
        product_inst = Product(product_name)

        if product_inst is not None:
            res = product.add_product(product_inst)
            if res is not None:
                return res
            else:
                return 'Failed to add product info'
        else:
            return 'None value'
    except Exception as e:
        print(e)
        return f'Exception {e} occurred'


def show_product_customers():
    try:
        product_id = request.args.get('product_id')

        res = product.show_customers_for_product(product_id)
        if res is not None:
            return res
        else:
            return "Couldn't show customers"
    except Exception as e:
        print(e)
        return f'Exception {e} occurred'
