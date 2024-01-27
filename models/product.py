import uuid

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

Base = sa.orm.declarative_base()


class Product(Base):
    __tablename__ = 'product'

    product_id = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    product_name = sa.Column(sa.Text, nullable=False)

    def __init__(self, product_name):
        self.product_name = product_name

    def __repr__(self):
        return f"{self.product_id} {self.product_name}"
