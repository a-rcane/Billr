-- Table: public.product

-- DROP TABLE IF EXISTS public.product;

CREATE TABLE IF NOT EXISTS public.product
(
    product_id uuid NOT NULL,
    product_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT product_pkey PRIMARY KEY (product_id),
    CONSTRAINT product_product_id_product_id1_key UNIQUE (product_id)
        INCLUDE(product_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.product
    OWNER to root;