-- Table: public.customer

-- DROP TABLE IF EXISTS public.customer;

CREATE TABLE IF NOT EXISTS public.customer
(
    customer_id uuid NOT NULL,
    customer_name text COLLATE pg_catalog."default" NOT NULL,
    customer_email character varying COLLATE pg_catalog."default" NOT NULL,
    cus_id character varying COLLATE pg_catalog."default",
    CONSTRAINT customer_pkey PRIMARY KEY (customer_id),
    CONSTRAINT customer_customer_id_customer_id1_key UNIQUE (customer_id)
        INCLUDE(customer_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customer
    OWNER to root;