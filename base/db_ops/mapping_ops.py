from flask import request

from base.db_ops.db_ops import DBOps
from configs.config import settings
from models.customer_product_map import CustomerProductMap


class MappingOperations(DBOps):
    def __init__(self, connection_string=settings.DB_URI):
        super().__init__(connection_string)

    def subscribe_customer_to_product(self, map_customer_product: CustomerProductMap):
        try:
            # product_id = request.args.get('product_id')
            # customer_id = request.args.get('customer_id')
            # map_customer_product = CustomerProductMap(product_id, customer_id)

            if map_customer_product is not None:
                with self.create_session() as s:
                    s.add(map_customer_product)
                    s.commit()
                    print(f'Customer {map_customer_product.customer_id} was subscribed to product {map_customer_product.product_id}')
                    s.close()
            else:
                print('Subscription failed')
                return None
        except Exception as e:
            print(e)


if __name__ == '__main__':
    map_ops = MappingOperations()
    map_inst = CustomerProductMap('99967654-e2f2-4523-b201-d1456b91a431', 'd3c80cdd-856b-47e5-b614-c8178b029888')
    map_ops.subscribe_customer_to_product(map_inst)
