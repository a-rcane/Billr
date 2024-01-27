from flask import request

from base.db_ops.db_ops import DBOps
from configs.config import settings
from models.customer_product_map import CustomerProductMap


class MappingOperations(DBOps):
    def __init__(self, connection_string=settings.DB_URI):
        super().__init__(connection_string)

    def subscribe_customer_to_product(self, map_customer_product: CustomerProductMap):
        try:
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
            return None

    def delete_by_customer_id(self, customer_id):
        try:
            if customer_id is not None:
                with self.create_session() as s:
                    s.query(CustomerProductMap).filter(CustomerProductMap.customer_id == customer_id).\
                        delete(synchronize_session='evaluate')
                    s.commit()
                    s.close()

                print('Successfully deleted mapping')
            else:
                print('Customer email was not provided')
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    map_ops = MappingOperations()
    map_inst = CustomerProductMap('99967654-e2f2-4523-b201-d1456b91a431', 'd3c80cdd-856b-47e5-b614-c8178b029888')
    map_ops.subscribe_customer_to_product(map_inst)
