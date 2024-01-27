-- Table: public.customer_product_map

-- DROP TABLE IF EXISTS public.customer_product_map;

CREATE TABLE IF NOT EXISTS public.customer_product_map
(
    map_id uuid NOT NULL,
    customer_id uuid NOT NULL,
    product_id uuid NOT NULL,
    CONSTRAINT customer_product_map_pkey PRIMARY KEY (map_id),
    CONSTRAINT customer_id FOREIGN KEY (customer_id)
        REFERENCES public.customer (customer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT product_id FOREIGN KEY (product_id)
        REFERENCES public.product (product_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customer_product_map
    OWNER to root;