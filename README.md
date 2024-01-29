# Billr

### About

This project simulates a two-way integration with a simple customer catalog and a customer catalog in
an external service - Stripe in this case. The two-way sync is near real-time so that 
a customer added/edited on one system propagates to the other system within a few seconds.

### Deployment Instructions

1. Clone the project 
    `https://github.com/a-rcane/Billr.git` locally
2. Run command `pip install -r requirements.txt` and `docker-compose up -d`
3. Run command `curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" 127.0.0.1:8083/connectors/ --data "@c
onfigs/debezium.json"` to start debezium-postgresql-connector 
4. Run command `winpty docker run -it --network=host edenhill/kcat:1.7.1 -b localhost:29092 -L` (use winpty if windows) for msg service 
5. Login into pgadmin on `localhost:5050` 
    using credentials `email: name@example.com` `password:admin`
6. Create server postgres with `user: root` `password: root`
7. Run queries as provided in `Billr/sql_scripts` directory to setup postgres 
8. Under `configs/settings.yaml` update values for `NGROK_API_KEY` `ENDPOINT_SECRET` `STRIPE_API_KEY`
9. Use the link in ngrok (url) as `url/stripe/webhook` and register this as endpoint on stripe 
10. Run `Billr\kafka_base\kafka_stripe.py` in one terminal
11. Run `app.py` then open ngrok and run `ngrok http 5000`



### APIs

1. `POST: /customers/add` adds customer `Params: customer_name, customer_email`\
***adds to stripe customers-list***
2. `GET: /customers/view-products` view products for specific customer `Params: customer_id`
3. `POST: /products/add` adds product to product db `Params: product_name`
4. `GET: /products/view-customer` view customers for specific product `Params: product_id`
5. `POST: /subscribe` adds product customer relation `Params: product_id, customer_id`


### Working
1. Adding a customer through endpoint updates stripe as well.
2. Adding, updating or deleting a customer on stripe makes the changes to local db as well.

This code can be extended to salesforce as well by adding the required webhooks and salesforce consumer method.