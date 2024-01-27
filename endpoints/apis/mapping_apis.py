from flask import request

from base.db_ops.mapping_ops import MappingOperations
from models.customer_product_map import CustomerProductMap

maps = MappingOperations()


def subscribe_method():
    try:
        product_id = request.args.get('product_id')
        customer_id = request.args.get('customer_id')
        map_customer_product = CustomerProductMap(product_id, customer_id)

        if map_customer_product is not None:
            res = maps.subscribe_customer_to_product(map_customer_product)
            if res is not None:
                return res
            else:
                return 'Subscription failed'
        else:
            return f'None value'
    except Exception as e:
        print(e)
        return f'Exception {e} occurred'
