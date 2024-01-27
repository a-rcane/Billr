import uuid

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker

from models.customer import Customer
from models.product import Product

Base = sa.orm.declarative_base()


class CustomerProductMap(Base):
    __tablename__ = 'customer_product_map'

    map_id = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    customer_id = sa.Column(sa.Uuid, ForeignKey(Customer.customer_id))
    product_id = sa.Column(sa.Uuid, ForeignKey(Product.product_id))

    def __init__(self, product_id, customer_id):
        self.product_id = product_id
        self.customer_id = customer_id

    def __repr__(self):
        return f"{self.map_id} {self.product_id} {self.customer_id}"
