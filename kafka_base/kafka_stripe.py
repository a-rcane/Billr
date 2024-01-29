import io
import avro
from avro.io import DatumReader, BinaryDecoder
from kafka import KafkaConsumer
import stripe
import os
from configs.config import settings


stripe.api_key = settings.get('STRIPE_API_KEY')


def data_reader():
    try:
        abs_path = os.path.dirname(__file__)
        file_path = os.path.join(abs_path, '..\\configs\\schema.avsc')
        schema = avro.schema.parse((open(file_path, "rb").read()).decode('utf-8'))
        reader = DatumReader(schema)
        return reader
    except Exception as e:
        print(e)
        return None


def decode(msg_value):
    try:
        message_bytes = io.BytesIO(msg_value)
        message_bytes.seek(7)
        decoder = BinaryDecoder(message_bytes)
        reader = data_reader()
        if reader is not None:
            event_dict = reader.read(decoder)
            return event_dict
        else:
            print('Reader returned None')
            return None
    except Exception as e:
        print(e)
        return None


def stripe_consumer():
    try:
        consumer = KafkaConsumer("postgres.public.customer", bootstrap_servers=["localhost:29092"])

        print('stripe consumer')
        print('Connected: ', consumer.bootstrap_connected())
        print('Subscription: ', consumer.subscription())

        for msg in consumer:
            data = decode(msg.value)
            if data is not None:
                if data['customer_status'] == 'CREATED':
                    add_stripe(data)
                if data['customer_status'] == 'UPDATED':
                    update_stripe(data)
                if data['customer_status'] == 'DELETED':
                    delete_stripe(data)
            else:
                print('Data is None')
    except Exception as e:
        print(str(e))
        return None


def add_stripe(data):
    try:
        print('stripe create')
        stripe.Customer.create(
            name=data['customer_name'],
            email=data['customer_email'],
        )
        print(f"Customer {data['customer_name']} published to stripe")
        return 'Customer added in stripe'
    except Exception as e:
        print(str(e))
        return None


def update_stripe(data):
    try:
        print('stripe update')
        if data['cus_id'] is not None:
            stripe.Customer.modify(
                data['cus_id'],
                name=data['customer_name'],
                email=data['customer_email'],
            )
            print(f"Customer {data['customer_name']} updated in stripe")
            return 'Customer updated in stripe'
        else:
            print(f"cus_id field is null")
            return None
    except Exception as e:
        print(str(e))
        return None


def delete_stripe(data: dict):
    try:
        print('stripe delete')
        if data['cus_id'] is not None:
            stripe.Customer.delete(data['cus_id'])
            return 'Customer deleted from stripe'
        else:
            print(f"cus_id field is null")
            return None
    except Exception as e:
        print(str(e))
        return None


if __name__ == '__main__':
    stripe_consumer()
