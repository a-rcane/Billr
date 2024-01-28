import io

import avro
from avro.io import DatumReader, BinaryDecoder
from kafka import KafkaConsumer
import stripe
import os
from configs.config import settings

abs_path = os.path.dirname(__file__)
file_path = os.path.join(abs_path, '..\\configs\\schema.avsc')
schema = avro.schema.parse((open(file_path, "rb").read()).decode('utf-8'))
reader = DatumReader(schema)


def decode(msg_value):
    message_bytes = io.BytesIO(msg_value)
    message_bytes.seek(7)
    decoder = BinaryDecoder(message_bytes)
    event_dict = reader.read(decoder)
    return event_dict


def stripe_consume():
    try:
        consumer = KafkaConsumer("postgres.public.customer",
                                 bootstrap_servers=["localhost:29092"])

        stripe.api_key = settings.get('STRIPE_API_KEY')
        for msg in consumer:
            data = decode(msg.value)
            print(data)
            stripe.Customer.create(
                name=data['customer_name'],
                email=data['customer_email'],
            )
            print(f"Customer {data['customer_name']} published to stripe")
            break
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    pass
