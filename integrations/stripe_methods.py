from base.db_ops.customer_ops import CustomerOperations
from base.db_ops.mapping_ops import MappingOperations
from models.customer import Customer

customer_ops = CustomerOperations()


def add_from_stripe(customer):
    try:
        if customer['name'] and customer['email'] is not None:
            existing = customer_ops.find_by_email(customer['email'])
            if existing is None:
                customer_inst = Customer(customer['name'], customer['email'])
                customer_ops.add_customer(customer_inst)
            else:
                print('Customer with this email already exists')
        else:
            print('Customer name/email was not provided')
    except Exception as e:
        print(e)
        return None


def update_from_stripe(customer):
    try:
        if customer['email'] is not None:
            existing = customer_ops.find_by_email(customer['email'])
            if existing is not None:
                customer_inst = Customer(customer['name'], customer['email'])
                customer_ops.update_customer_by_email(customer_inst)
            else:
                print('This email is not registered')
        else:
            print('Customer email was not provided')
    except Exception as e:
        print(e)
        return None


def delete_from_stripe(customer):
    try:
        if customer['email'] is not None:
            existing = customer_ops.find_by_email(customer['email'])
            if existing is not None:
                mapping_ops = MappingOperations()
                new_customer_ops = CustomerOperations()
                mapping_ops.delete_by_customer_id(existing['customer_id'])
                new_customer_ops.delete_customer_by_email(customer['email'])
            else:
                print('This email is not registered')
        else:
            print('Customer email was not provided')
    except Exception as e:
        print(e)
        return None
