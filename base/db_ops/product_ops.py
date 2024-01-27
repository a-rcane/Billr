from base.db_ops.db_ops import DBOps
from configs.config import settings
from models.customer_product_map import CustomerProductMap
from models.product import Product


class ProductOperations(DBOps):
    def __init__(self, connection_string=settings.DB_URI):
        super().__init__(connection_string)

    def get_name_by_id(self, product_id):
        try:
            with self.create_session() as s:
                p = s.query(Product).filter(Product.product_id == product_id).first()
                s.close()
            if p is not None:
                return p.product_name
            else:
                return f'No product for specified id {product_id} exists'
        except Exception as e:
            print(e)
            return None

    def add_product(self, product_inst: Product):
        try:
            if product_inst is not None:
                with self.create_session() as s:
                    s.add(product_inst)
                    s.commit()
                    print(f'Customer {product_inst.product_name} added to db')
                    s.close()
            else:
                print('Product was not added')
                return None
        except Exception as e:
            print(e)
            return None

    def show_customers_for_product(self, product_id):
        try:
            with self.create_session() as s:
                p = s.query(CustomerProductMap).filter(CustomerProductMap.product_id == product_id).all()
                s.close()
            if p is not None and len(p) > 0:
                from base.db_ops.customer_ops import CustomerOperations
                res = []
                customer = CustomerOperations()
                for val in p:
                    res.append({
                        'customer_id': val.customer_id,
                        'customer_name': customer.get_name_by_id(val.customer_id),
                    })
                # print({'product_id': product_id, 'customers': res})
                return {
                    'product_id': product_id,
                    'customers': res
                }
            else:
                print(f'No customers found for {product_id}')
                return None
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    product_ops = ProductOperations()
    # product = Product('Mobile')
    # product_ops.add_product(product)
    product_ops.show_customers_for_product('99967654-e2f2-4523-b201-d1456b91a431')
