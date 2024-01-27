from base.db_ops.db_ops import DBOps
from configs.config import settings


class ProductOperations(DBOps):
    def __init__(self, connection_string=settings.DB_URI):
        super().__init__(connection_string)
