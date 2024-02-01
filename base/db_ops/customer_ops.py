import time

from base.db_ops.db_ops import DBOps
from configs.config import settings
from models.customer import Customer
from models.customer_product_map import CustomerProductMap


class CustomerOperations(DBOps):
    def __init__(self, connection_string=settings.DB_URI):
        super().__init__(connection_string)

    def get_name_by_id(self, customer_id):
        try:
            with self.create_session() as s:
                p = s.query(Customer).filter(Customer.customer_id == customer_id).first()
                s.close()
            if p is not None:
                return p.customer_name
            else:
                print(f'No customer for specified id {customer_id} exists')
                return None
        except Exception as e:
            print(e)
            return None

    def show_products_for_customer(self, customer_id):
        try:
            with self.create_session() as s:
                p = s.query(CustomerProductMap).filter(CustomerProductMap.customer_id == customer_id).all()
                s.close()
            if p is not None and len(p) > 0:
                from base.db_ops.product_ops import ProductOperations
                res = []
                product = ProductOperations()
                for val in p:
                    res.append({
                        'product_id': val.product_id,
                        'product_name': product.get_name_by_id(val.product_id),
                    })
                # print({'customer_id': customer_id, 'products': res})
                return {
                    'customer_id': customer_id,
                    'products': res
                }
            else:
                print(f'No product found for Customer {customer_id}')
                return None
        except Exception as e:
            print(e)
            return None

    def find_by_email(self, customer_email):
        try:
            with self.create_session() as s:
                p = s.query(Customer).filter(Customer.customer_email == customer_email).first()
                s.close()
            if p is not None and p.customer_status != 'DELETED':
                return {
                    'customer_id': p.customer_id,
                    'customer_name': p.customer_name,
                    'customer_email': p.customer_email,
                    'cus_id': p.cus_id,
                    'customer_status': p.customer_status
                }
            else:
                print('Email does not belong to a registered customer')
                return None
        except Exception as e:
            print(e)
            return None

    def update_customer(self, customer_inst: Customer):
        try:
            if customer_inst is not None:
                p = self.find_by_email(customer_inst.customer_email)
                if p is None:
                    return "Customer doesn't exist"
                else:
                    if customer_inst.cus_id is not None:
                        cus_id = customer_inst.cus_id
                    else:
                        cus_id = p['cus_id']
                    with self.create_session() as s:
                        s.query(Customer).filter(Customer.customer_email == customer_inst.customer_email).\
                            update({
                                'customer_name': customer_inst.customer_name,
                                'customer_email': customer_inst.customer_email,
                                'cus_id': cus_id,
                                'customer_status': customer_inst.customer_status
                            })
                        s.commit()
                        s.close()
                    return 'Customer updated'
            else:
                print('Customer was not added')
                return None
        except Exception as e:
            print(e)
            return None

    def add_customer(self, customer_inst: Customer):
        try:
            if customer_inst is not None:
                p = self.find_by_email(customer_inst.customer_email)
                if p is None:
                    with self.create_session() as s:
                        s.add(customer_inst)
                        s.commit()
                    return {
                        'customer_id': customer_inst.customer_id,
                        'customer_name': customer_inst.customer_name,
                        'customer_email': customer_inst.customer_email,
                        'customer_status': customer_inst.customer_status,
                    }
                else:
                    print('Customer already exists')
            else:
                print('Customer was not added')
                return None
        except Exception as e:
            print(e)
            return None

    def delete_customer(self, customer_email):
        try:
            existing = self.find_by_email(customer_email)
            if existing is None:
                return "Customer doesn't exist"
            else:
                with self.create_session() as s:
                    s.query(Customer).filter(Customer.customer_email == customer_email). \
                            update({
                                'customer_status': 'DELETED',
                            })
                    s.commit()
                    print('Successfully deleted customer details')
                    s.close()
                return f'Successfully deleted customer details for {customer_email}'
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    customer_ops = CustomerOperations()
    # customer = Customer('abc', 'abc@gmail.com')
    # customer_ops.add_customer(customer)
    customer_ops.show_products_for_customer('d3c80cdd-856b-47e5-b614-c8178b029888')
