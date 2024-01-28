from base.utils import create_app
from configs.config import settings
from endpoints.apis import customer_apis, product_apis, mapping_apis
from endpoints.webhooks import stripe_webhook

app = create_app()
app.config['SECRET_KEY'] = settings.get('secret_key')


@app.route('/')
def ping():
    return 'ping!'


# apis
'--------------------------------------------------------------------------------------------------------------------'
app.add_url_rule('/customers/add', view_func=customer_apis.add_customer_info, methods=['POST'])
app.add_url_rule('/customers/update', view_func=customer_apis.delete_customer_info, methods=['PUT'])
app.add_url_rule('/customers/delete', view_func=customer_apis.update_customer_info, methods=['DELETE'])
app.add_url_rule('/customers/view-products', view_func=customer_apis.show_customer_products, methods=['GET'])

app.add_url_rule('/products/add', view_func=product_apis.add_product_info, methods=['POST'])
app.add_url_rule('/products/view-customers', view_func=product_apis.show_product_customers, methods=['GET'])

app.add_url_rule('/subscribe', view_func=mapping_apis.subscribe_method, methods=['POST'])
'--------------------------------------------------------------------------------------------------------------------'

# webhooks
'--------------------------------------------------------------------------------------------------------------------'
app.add_url_rule('/stripe/webhook', view_func=stripe_webhook.webhook, methods=['POST'])
'--------------------------------------------------------------------------------------------------------------------'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
