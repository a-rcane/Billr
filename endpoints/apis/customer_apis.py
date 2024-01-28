from flask import request

from base.db_ops.customer_ops import CustomerOperations
from models.customer import Customer

customer = CustomerOperations()


def add_customer_info():
    try:
        customer_name = request.args.get('customer_name')
        customer_email = request.args.get('customer_email')
        customer_inst = Customer(customer_name, customer_email, '')
        if customer_inst is not None:
            res = customer.add_customer(customer_inst)
            if res is not None:
                return res
            else:
                return 'Failed to add customer info'
        else:
            return f'None value'
    except Exception as e:
        print(e)
        return f'Exception {e} occurred'


def update_customer_info():
    try:
        customer_name = request.args.get('customer_name')
        customer_email = request.args.get('customer_email')
        customer_inst = Customer(customer_name, customer_email, '')
        if customer_inst is not None:
            res = customer.update_customer(customer_inst)
            if res is not None:
                return res
            else:
                return 'Failed to update customer info'
        else:
            return f'None value'
    except Exception as e:
        print(e)
        return f'Exception {e} occurred'


def delete_customer_info():
    try:
        customer_email = request.args.get('customer_email')
        if customer_email is not None:
            res = customer.delete_customer(customer_email)
            if res is not None:
                return res
            else:
                return 'Failed to delete customer info'
        else:
            return f'None value'
    except Exception as e:
        print(e)
        return f'Exception {e} occurred'


def show_customer_products():
    try:
        customer_id = request.args.get('customer_id')

        res = customer.show_products_for_customer(customer_id)
        if res is not None:
            return res
        else:
            return "Couldn't show products"
    except Exception as e:
        print(e)
        return f'Exception {e} occurred'
