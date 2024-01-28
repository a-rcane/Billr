import uuid

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from base.db_ops.db_ops import DBOps

Base = sa.orm.declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = sa.Column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    customer_name = sa.Column(sa.Text, nullable=False)
    customer_email = sa.Column(sa.VARCHAR, nullable=False)
    cus_id = sa.Column(sa.VARCHAR)

    def __init__(self, customer_name, customer_email, cus_id):
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.cus_id = cus_id

    def __repr__(self):
        return f"{self.customer_id} {self.customer_name} {self.customer_email} {self.cus_id}"


if __name__ == '__main__':
    with DBOps().create_session() as s:
        c = Customer('User', 'user@gmail.com')
        try:
            # s.add(c)
            # s.commit()
            print('Customer added to db')
            s.close()
        except Exception as e:
            print(e)
            s.rollback()
