--
-- PostgreSQL database dump
--

\restrict v4Pj0tiENcxp06dmfDU0Kipj02ljGvedzLwZW5kSEZmgLZKVfdIjzZgl4yLA1kF

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: notification_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notification_type AS ENUM (
    'order_confirmation',
    'payment_success',
    'payment_failed',
    'order_shipped'
);


ALTER TYPE public.notification_type OWNER TO postgres;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.userrole AS ENUM (
    'user',
    'admin',
    'superadmin'
);


ALTER TYPE public.userrole OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_items (
    id uuid NOT NULL,
    product_id uuid,
    quantity integer NOT NULL,
    price_at_add numeric(10,2) NOT NULL,
    cart_id uuid
);


ALTER TABLE public.cart_items OWNER TO postgres;

--
-- Name: carts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carts (
    id uuid NOT NULL,
    user_id uuid,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.carts OWNER TO postgres;

--
-- Name: notification_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_messages (
    id uuid NOT NULL,
    notification_id uuid NOT NULL,
    related_type character varying,
    related_id uuid,
    type public.notification_type NOT NULL,
    title character varying NOT NULL,
    body character varying NOT NULL,
    is_read boolean,
    created_at timestamp with time zone
);


ALTER TABLE public.notification_messages OWNER TO postgres;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id uuid NOT NULL,
    order_id uuid NOT NULL,
    product_id uuid NOT NULL,
    quantity integer NOT NULL,
    price_at_purchase numeric(10,2) NOT NULL,
    product_name character varying NOT NULL
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    address_id uuid NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    status character varying NOT NULL,
    created_at timestamp with time zone
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    id uuid NOT NULL,
    order_id uuid,
    user_id uuid,
    stripe_session_id character varying NOT NULL,
    stripe_payment_intent_id character varying,
    amount numeric(10,2) NOT NULL,
    currency character varying(3),
    status character varying NOT NULL,
    payment_method character varying,
    raw_response json,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id uuid NOT NULL,
    name character varying NOT NULL,
    description character varying,
    price numeric(10,2) NOT NULL,
    stock integer,
    is_active boolean,
    created_at timestamp with time zone,
    sku character varying,
    updated_at timestamp with time zone
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: refunds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refunds (
    id uuid NOT NULL,
    order_id uuid NOT NULL,
    payment_id uuid NOT NULL,
    stripe_refund_id character varying,
    amount numeric(10,2) NOT NULL,
    status character varying,
    fee_deducted numeric(10,2),
    cancellation_reason character varying,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.refunds OWNER TO postgres;

--
-- Name: user_addresses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_addresses (
    id uuid NOT NULL,
    user_id uuid,
    full_name character varying NOT NULL,
    phone character varying NOT NULL,
    address_line1 character varying NOT NULL,
    address_line2 character varying,
    city character varying NOT NULL,
    pincode character varying NOT NULL,
    address_type character varying NOT NULL,
    created_at timestamp with time zone,
    is_default boolean
);


ALTER TABLE public.user_addresses OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    password character varying,
    role public.userrole,
    is_active boolean,
    is_verified boolean,
    created_at timestamp with time zone,
    provider character varying,
    provider_id character varying,
    updated_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
ce3216427142
\.


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_items (id, product_id, quantity, price_at_add, cart_id) FROM stdin;
\.


--
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.carts (id, user_id, created_at, updated_at) FROM stdin;
6a53c986-9ca7-4bcc-85cf-dc59231dce54	dc34a575-f659-4468-8cc4-8b051a548507	2025-12-17 04:15:45.730604+05:30	2025-12-17 04:15:45.730609+05:30
5a9d0ab0-4ffd-4941-bcb2-8fa67c469eb4	f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	2025-12-29 04:56:12.26348+05:30	2025-12-29 04:56:12.263484+05:30
e45ee6a1-5f8f-416d-855e-7958a9b44f23	d4520075-f4c8-4843-874f-e22fd30b9414	2025-12-30 04:14:56.838405+05:30	2025-12-30 04:14:56.838409+05:30
\.


--
-- Data for Name: notification_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_messages (id, notification_id, related_type, related_id, type, title, body, is_read, created_at) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, created_at) FROM stdin;
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, product_id, quantity, price_at_purchase, product_name) FROM stdin;
e6814708-c8dc-4b4f-82ac-e8ac1a539bff	2440a3aa-f816-4882-9095-d0c946b0d137	94c0166a-371d-4401-8558-131365bbb6a3	1	1599.99	iPhone 16 Pro
c7055416-1b9e-491f-a0be-c7f58df368f0	169e8920-da5b-4ac6-8f17-63df29c7e544	94c0166a-371d-4401-8558-131365bbb6a3	2	1599.99	iPhone 16 Pro
8cfd3ad3-8f59-463e-a84c-395507fdfc06	b8d54991-f2cc-429b-9f95-c3028d571a3b	94c0166a-371d-4401-8558-131365bbb6a3	2	1599.99	iPhone 16 Pro
98833d71-3921-4103-afc5-ee7d7b85ff34	54d93617-f9cc-497b-883c-9c4e15b89d55	94c0166a-371d-4401-8558-131365bbb6a3	2	1599.99	iPhone 16 Pro
f8fce8b5-7ebc-4557-bd74-9eacf9fb9b49	ae845918-0e3b-4a49-aeb0-9af6e5ef0758	94c0166a-371d-4401-8558-131365bbb6a3	1	1599.99	iPhone 16 Pro
b086a0b9-6e74-456b-b85b-91347c9edec3	82c9d54a-d486-4742-8512-7f169b800ba2	94c0166a-371d-4401-8558-131365bbb6a3	1	1599.99	iPhone 16 Pro
d6f71a2e-22e5-4a29-a775-4cfef4f42bb7	6cab1798-a27f-4de7-8225-378eb584352b	94c0166a-371d-4401-8558-131365bbb6a3	1	1599.99	iPhone 16 Pro
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, user_id, address_id, total_amount, status, created_at) FROM stdin;
2440a3aa-f816-4882-9095-d0c946b0d137	dc34a575-f659-4468-8cc4-8b051a548507	aff775dc-25ea-4109-9de0-9a0af11076d0	1599.99	paid	2025-12-22 11:21:20.710296+05:30
169e8920-da5b-4ac6-8f17-63df29c7e544	f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	aff775dc-25ea-4109-9de0-9a0af11076d0	3199.98	paid	2025-12-29 04:58:57.202436+05:30
b8d54991-f2cc-429b-9f95-c3028d571a3b	f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	aff775dc-25ea-4109-9de0-9a0af11076d0	3199.98	cancelled	2025-12-29 07:09:10.912337+05:30
54d93617-f9cc-497b-883c-9c4e15b89d55	f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	aff775dc-25ea-4109-9de0-9a0af11076d0	3199.98	pending	2025-12-30 04:05:26.088998+05:30
ae845918-0e3b-4a49-aeb0-9af6e5ef0758	d4520075-f4c8-4843-874f-e22fd30b9414	aff775dc-25ea-4109-9de0-9a0af11076d0	1599.99	paid	2025-12-30 04:23:23.932752+05:30
82c9d54a-d486-4742-8512-7f169b800ba2	d4520075-f4c8-4843-874f-e22fd30b9414	aff775dc-25ea-4109-9de0-9a0af11076d0	1599.99	pending	2026-01-05 05:44:59.925139+05:30
6cab1798-a27f-4de7-8225-378eb584352b	d4520075-f4c8-4843-874f-e22fd30b9414	aff775dc-25ea-4109-9de0-9a0af11076d0	1599.99	paid	2026-01-05 05:50:31.986035+05:30
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, order_id, user_id, stripe_session_id, stripe_payment_intent_id, amount, currency, status, payment_method, raw_response, created_at, updated_at) FROM stdin;
fe14aa6f-ea7b-4a92-8b5e-11a1d7682509	2440a3aa-f816-4882-9095-d0c946b0d137	dc34a575-f659-4468-8cc4-8b051a548507	cs_test_a1lf5nh0DR3hFOo9aSVXo2m9jrJwvHyrkzpc0rJL5jamaLhY0UBeugFQ0D	pi_mock_12345	1599.99	INR	succeeded	card	{"type": "checkout.session.completed", "data": {"object": {"id": "cs_test_a1lf5nh0DR3hFOo9aSVXo2m9jrJwvHyrkzpc0rJL5jamaLhY0UBeugFQ0D", "payment_intent": "pi_mock_12345", "metadata": {"order_id": "2440a3aa-f816-4882-9095-d0c946b0d137"}}}}	2025-12-23 13:25:50.885562+05:30	2025-12-23 14:25:06.892363+05:30
755f3c60-af04-4e9a-b052-2ea441bb2731	169e8920-da5b-4ac6-8f17-63df29c7e544	f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	cs_test_a12j6AsOq44PGw12dWaznaKBzrV50TNnI9zMg99mfhjBpE3OJbktAZbcEw	pi_mock_1	3199.98	INR	succeeded	card	{"type": "checkout.session.completed", "data": {"object": {"id": "cs_test_a12j6AsOq44PGw12dWaznaKBzrV50TNnI9zMg99mfhjBpE3OJbktAZbcEw", "payment_intent": "pi_mock_1", "metadata": {"order_id": "169e8920-da5b-4ac6-8f17-63df29c7e544"}}}}	2025-12-29 10:30:01.657641+05:30	2025-12-29 10:34:56.75063+05:30
6d8deb51-58ca-457a-830a-f642582406e8	b8d54991-f2cc-429b-9f95-c3028d571a3b	f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	cs_test_a1WG4keVLzyyWvdMNpGEtbOVM3vHlFuW8QgXCqr9HhHk6Uean67oRFnIoQ	pi_3SjacWQV9XNJzbbQ5APvMmTX	3199.98	INR	refunded	card	{"type": "checkout.session.completed", "data": {"object": {"id": "cs_test_a1WG4keVLzyyWvdMNpGEtbOVM3vHlFuW8QgXCqr9HhHk6Uean67oRFnIoQ", "payment_intent": "pi_3Qxxxxxxxxxxxx", "payment_method_types": ["card"], "metadata": {"order_id": "b8d54991-f2cc-429b-9f95-c3028d571a3b"}}}}	2025-12-29 12:40:42.473327+05:30	2025-12-29 12:58:48.582697+05:30
0af5114e-7cb8-4842-b327-9ba6a65faccb	ae845918-0e3b-4a49-aeb0-9af6e5ef0758	d4520075-f4c8-4843-874f-e22fd30b9414	cs_test_a1ckk8L82M75nKcVvMmBBJ1iNx1yzBih8VwfXaQlM9udZplzdGilk3DlV2	pi_3SjvHPQV9XNJzbbQ13otsNoN	1599.99	INR	succeeded	card	{"type": "checkout.session.completed", "data": {"object": {"id": "cs_test_a1ckk8L82M75nKcVvMmBBJ1iNx1yzBih8VwfXaQlM9udZplzdGilk3DlV2", "payment_intent": "pi_3SjvHPQV9XNJzbbQ13otsNoN", "payment_method_types": ["card"], "metadata": {"order_id": "ae845918-0e3b-4a49-aeb0-9af6e5ef0758"}}}}	2025-12-30 10:44:53.658879+05:30	2025-12-30 10:49:46.88282+05:30
2cf7d38d-25a3-4dd3-b3f9-a7b36a8ac9b6	6cab1798-a27f-4de7-8225-378eb584352b	d4520075-f4c8-4843-874f-e22fd30b9414	cs_test_a1OSjTEScQV8QhPz7qVJH5mqry9dyvVrV6FUsALd9rAgd1NAoigqcZ4BGy	\N	1599.99	INR	pending	\N	\N	2026-01-05 11:23:29.184261+05:30	\N
7bd9506c-05fb-4966-a433-c6f6e8d33c90	6cab1798-a27f-4de7-8225-378eb584352b	d4520075-f4c8-4843-874f-e22fd30b9414	cs_test_a1QvjA2Hhk9h66ZE8qwzLRbcD8WiBdrCmVkMQmbGz5uz44DlQzEImRHYbg	\N	1599.99	INR	pending	\N	\N	2026-01-05 11:26:10.516788+05:30	\N
1579341f-d374-41ca-8351-ef35142158e4	6cab1798-a27f-4de7-8225-378eb584352b	d4520075-f4c8-4843-874f-e22fd30b9414	cs_test_a1gYTcwOWolqrRVf8vCDcPwR7d3d6j7lKxzI0l7tv7qlMkrrpmMpg4AYIu	\N	1599.99	INR	pending	\N	\N	2026-01-05 11:30:38.8246+05:30	\N
35ee3d84-c6d5-4825-9481-962ee1228455	6cab1798-a27f-4de7-8225-378eb584352b	d4520075-f4c8-4843-874f-e22fd30b9414	cs_test_a1idTTTq6bo2noNTHFFSBHMrhJzV2XFeC6YH0RFOBm0WnKxEeilgiF4ivN	pi_3Sm6snQV9XNJzbbQ3TZbnMVK	1599.99	INR	succeeded	card	{"id": "evt_1Sm6soQV9XNJzbbQ1ZG3vHm5", "object": "event", "api_version": "2025-12-15.clover", "created": 1767592994, "data": {"object": {"id": "cs_test_a1idTTTq6bo2noNTHFFSBHMrhJzV2XFeC6YH0RFOBm0WnKxEeilgiF4ivN", "object": "checkout.session", "adaptive_pricing": {"enabled": true}, "after_expiration": null, "allow_promotion_codes": null, "amount_subtotal": 159999, "amount_total": 159999, "automatic_tax": {"enabled": false, "liability": null, "provider": null, "status": null}, "billing_address_collection": null, "branding_settings": {"background_color": "#ffffff", "border_style": "rounded", "button_color": "#0074d4", "display_name": "", "font_family": "default", "icon": null, "logo": null}, "cancel_url": "http://localhost:8000/payments/cancel", "client_reference_id": null, "client_secret": null, "collected_information": {"business_name": null, "individual_name": null, "shipping_details": null}, "consent": null, "consent_collection": null, "created": 1767592977, "currency": "inr", "currency_conversion": null, "custom_fields": [], "custom_text": {"after_submit": null, "shipping_address": null, "submit": null, "terms_of_service_acceptance": null}, "customer": null, "customer_account": null, "customer_creation": "if_required", "customer_details": {"address": {"city": null, "country": "IN", "line1": null, "line2": null, "postal_code": null, "state": null}, "business_name": null, "email": "akshatchauhan2532@gmail.com", "individual_name": null, "name": "Akshat chauhan", "phone": null, "tax_exempt": "none", "tax_ids": []}, "customer_email": "akshatchauhan2532@gmail.com", "discounts": [], "expires_at": 1767679377, "invoice": null, "invoice_creation": {"enabled": false, "invoice_data": {"account_tax_ids": null, "custom_fields": null, "description": null, "footer": null, "issuer": null, "metadata": {}, "rendering_options": null}}, "livemode": false, "locale": null, "metadata": {"order_id": "6cab1798-a27f-4de7-8225-378eb584352b"}, "mode": "payment", "origin_context": null, "payment_intent": "pi_3Sm6snQV9XNJzbbQ3TZbnMVK", "payment_link": null, "payment_method_collection": "if_required", "payment_method_configuration_details": null, "payment_method_options": {"card": {"request_three_d_secure": "automatic"}}, "payment_method_types": ["card"], "payment_status": "paid", "permissions": null, "phone_number_collection": {"enabled": false}, "recovered_from": null, "saved_payment_method_options": null, "setup_intent": null, "shipping_address_collection": null, "shipping_cost": null, "shipping_options": [], "status": "complete", "submit_type": null, "subscription": null, "success_url": "http://localhost:8000/payments/success", "total_details": {"amount_discount": 0, "amount_shipping": 0, "amount_tax": 0}, "ui_mode": "hosted", "url": null, "wallet_options": null}}, "livemode": false, "pending_webhooks": 1, "request": {"id": null, "idempotency_key": null}, "type": "checkout.session.completed"}	2026-01-05 11:32:56.911425+05:30	2026-01-05 11:33:14.898732+05:30
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, name, description, price, stock, is_active, created_at, sku, updated_at) FROM stdin;
4fb1cda9-ce2f-4a5e-9878-352feb128f7d	iPhone 15 Pro	Apple iPhone 15 Pro with A17 chip	1299.99	46	t	2025-12-15 17:19:01.458323+05:30	\N	\N
94c0166a-371d-4401-8558-131365bbb6a3	iPhone 16 Pro	Apple iPhone 16 Pro with A18 chip	1599.99	16	t	2025-12-16 09:06:17.56396+05:30	\N	\N
\.


--
-- Data for Name: refunds; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refunds (id, order_id, payment_id, stripe_refund_id, amount, status, fee_deducted, cancellation_reason, created_at) FROM stdin;
\.


--
-- Data for Name: user_addresses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_addresses (id, user_id, full_name, phone, address_line1, address_line2, city, pincode, address_type, created_at, is_default) FROM stdin;
c775c3be-f717-4499-8d14-8fbd0a2c07a4	dc34a575-f659-4468-8cc4-8b051a548507	Akshat Chauhan	9876543210	Flat 302, Green Residency	Near City Mall	Bengaluru	560001	home	2025-12-18 07:35:27.593135+05:30	f
aff775dc-25ea-4109-9de0-9a0af11076d0	dc34a575-f659-4468-8cc4-8b051a548507	Akshat Chauhan	9876543210	Flat 302, Green Residency	Near City Mall	Bengaluru	560003	home	2025-12-18 08:59:47.195498+05:30	t
56db2c9c-c428-4aba-8931-8cf634b8b35a	f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	Akshat Chauhan	8505845038	Balbir Nagar	Near Durgpuri Chowk	Delhi	110032	home	2025-12-29 04:58:34.175104+05:30	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, role, is_active, is_verified, created_at, provider, provider_id, updated_at) FROM stdin;
83f749da-2563-4602-b27f-efe6d8483471	string	user@example.com	$2b$12$MRoAk9n7cMAaMlntPZaUm.rXymmhwdQ2mZO7CDU57Cl1DbrI15wWW	superadmin	t	f	2025-12-11 05:33:22.625677+05:30	\N	\N	\N
0bef894c-8da2-4649-b67a-94514b661b57	sstring	suser@example.com	$2b$12$So.KYLuWNZ9NTB9rNE/QoeJH59M93.0RtXk.oXhiEfUqFQBLcDZAC	user	t	f	2025-12-15 10:38:07.47803+05:30	local	\N	\N
4d7c876c-f813-43f2-82ee-447f07fe1a9e	akshat	akshat@gmail.com	$2b$12$FZCAbAgJbzPsI9W94QEefexo8HqVDL4TevwM7cexSMFK7qo/NjGpu	admin	t	f	2025-12-15 11:53:17.38512+05:30	local	\N	\N
dc34a575-f659-4468-8cc4-8b051a548507	test	test@gmail.com	$2b$12$MadW5/d9w5yahLkcuuTIUuLa6NWHEEmUEoDZF3JvivpoL8U8GODla	user	t	f	2025-12-16 09:07:11.047189+05:30	local	\N	\N
f7e3e3bf-484c-4af4-bd96-8adb3a3d6cd3	dev	dev@gmail.com	$2b$12$qmVbeWGXQmI.QkinAbRbFOjKKQx/iN81k6Bwoab18ZH4d1CBUZVwi	user	t	f	2025-12-29 04:55:01.505344+05:30	local	\N	2025-12-29 04:55:01.505348+05:30
d4520075-f4c8-4843-874f-e22fd30b9414	akshat	akshatchauhan2532@gmail.com	$2b$12$YM3eWkNlzEZm0NJU27m5R.DdRaFCm.flwwjSz.f/wBab/Ev0fdWR.	user	t	f	2025-12-30 04:14:06.826267+05:30	local	\N	2025-12-30 04:14:06.82627+05:30
e77cd0b6-e65c-474d-a344-9df85dbbbd50	event manage	eventmanagementmail25@gmail.com	\N	user	t	t	2025-12-30 08:58:02.416598+05:30	google	106944090146392548466	2025-12-30 08:58:02.416604+05:30
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);


--
-- Name: carts carts_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_user_id_key UNIQUE (user_id);


--
-- Name: notification_messages notification_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_messages
    ADD CONSTRAINT notification_messages_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: refunds refunds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_pkey PRIMARY KEY (id);


--
-- Name: refunds refunds_stripe_refund_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_stripe_refund_id_key UNIQUE (stripe_refund_id);


--
-- Name: cart_items uq_cart_product; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT uq_cart_product UNIQUE (cart_id, product_id);


--
-- Name: user_addresses user_addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_addresses
    ADD CONSTRAINT user_addresses_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_order_items_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_order_id ON public.order_items USING btree (order_id);


--
-- Name: ix_orders_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_user_id ON public.orders USING btree (user_id);


--
-- Name: ix_payments_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payments_order_id ON public.payments USING btree (order_id);


--
-- Name: ix_payments_stripe_payment_intent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_payments_stripe_payment_intent_id ON public.payments USING btree (stripe_payment_intent_id);


--
-- Name: ix_payments_stripe_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_payments_stripe_session_id ON public.payments USING btree (stripe_session_id);


--
-- Name: ix_payments_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payments_user_id ON public.payments USING btree (user_id);


--
-- Name: ix_products_sku; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_products_sku ON public.products USING btree (sku);


--
-- Name: ix_user_addresses_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_addresses_phone ON public.user_addresses USING btree (phone);


--
-- Name: ix_user_addresses_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_addresses_user_id ON public.user_addresses USING btree (user_id);


--
-- Name: ix_user_default_address; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_default_address ON public.user_addresses USING btree (user_id, is_default);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_is_active ON public.users USING btree (is_active);


--
-- Name: ix_users_provider; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_provider ON public.users USING btree (provider);


--
-- Name: ix_users_provider_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_provider_id ON public.users USING btree (provider_id);


--
-- Name: cart_items cart_items_cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES public.carts(id) ON DELETE CASCADE;


--
-- Name: cart_items cart_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: carts carts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notification_messages notification_messages_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_messages
    ADD CONSTRAINT notification_messages_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.notifications(id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE RESTRICT;


--
-- Name: orders orders_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.user_addresses(id) ON DELETE RESTRICT;


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: payments payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE SET NULL;


--
-- Name: payments payments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: refunds refunds_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: refunds refunds_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id) ON DELETE CASCADE;


--
-- Name: user_addresses user_addresses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_addresses
    ADD CONSTRAINT user_addresses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict v4Pj0tiENcxp06dmfDU0Kipj02ljGvedzLwZW5kSEZmgLZKVfdIjzZgl4yLA1kF

