import io
import avro
from avro.io import DatumReader, BinaryDecoder
from kafka import KafkaConsumer
import stripe
import os
from configs.config import settings
from models.customer import Customer

abs_path = os.path.dirname(__file__)
file_path = os.path.join(abs_path, '..\\configs\\schema.avsc')
schema = avro.schema.parse((open(file_path, "rb").read()).decode('utf-8'))
reader = DatumReader(schema)

stripe.api_key = settings.get('STRIPE_API_KEY')


def decode(msg_value):
    message_bytes = io.BytesIO(msg_value)
    message_bytes.seek(7)
    decoder = BinaryDecoder(message_bytes)
    event_dict = reader.read(decoder)
    return event_dict


def stripe_add_consume():
    try:
        consumer = KafkaConsumer("postgres.public.customer", bootstrap_servers=["localhost:29092"])
        print('stripe consume')
        for msg in consumer:
            data = decode(msg.value)
            stripe.Customer.create(
                name=data['customer_name'],
                email=data['customer_email'],
            )
            print(f"Customer {data['customer_name']} published to stripe")
            break
    except Exception as e:
        print(str(e))
        return None


def stripe_update_consume(customer_inst: Customer):
    try:
        consumer = KafkaConsumer("postgres.public.customer", bootstrap_servers=["localhost:29092"])

        for msg in consumer:
            data = decode(msg.value)
            stripe.Customer.modify(
                customer_inst.cus_id,
                name=data['customer_name'],
                email=data['customer_email'],
            )
            print(f"Customer {data['customer_name']} updated in stripe")
            break
    except Exception as e:
        print(str(e))
        return None


def stripe_delete_consume(cus_id):
    try:
        consumer = KafkaConsumer("postgres.public.customer", bootstrap_servers=["localhost:29092"])
        for msg in consumer:
            data = decode(msg.value)
            stripe.Customer.delete(cus_id)
            print(f"Customer {data['customer_name']} deleted in stripe")
            break
    except Exception as e:
        print(str(e))
        return None


if __name__ == '__main__':
    pass
