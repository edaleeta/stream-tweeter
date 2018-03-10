--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: base_templates; Type: TABLE; Schema: public; Owner: edaleeta
--

CREATE TABLE base_templates (
    template_id integer NOT NULL,
    contents text NOT NULL
);


ALTER TABLE base_templates OWNER TO edaleeta;

--
-- Name: base_templates_template_id_seq; Type: SEQUENCE; Schema: public; Owner: edaleeta
--

CREATE SEQUENCE base_templates_template_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE base_templates_template_id_seq OWNER TO edaleeta;

--
-- Name: base_templates_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: edaleeta
--

ALTER SEQUENCE base_templates_template_id_seq OWNED BY base_templates.template_id;


--
-- Name: base_templates template_id; Type: DEFAULT; Schema: public; Owner: edaleeta
--

ALTER TABLE ONLY base_templates ALTER COLUMN template_id SET DEFAULT nextval('base_templates_template_id_seq'::regclass);


--
-- Data for Name: base_templates; Type: TABLE DATA; Schema: public; Owner: edaleeta
--

COPY base_templates (template_id, contents) FROM stdin;
1	I'm live on Twitch!\r\nJoin me here: ${url}.
2	We're playing ${game}!\r\nJoin me on Twitch: ${url}.
\.


--
-- Name: base_templates_template_id_seq; Type: SEQUENCE SET; Schema: public; Owner: edaleeta
--

SELECT pg_catalog.setval('base_templates_template_id_seq', 2, true);


--
-- Name: base_templates base_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: edaleeta
--

ALTER TABLE ONLY base_templates
    ADD CONSTRAINT base_templates_pkey PRIMARY KEY (template_id);


--
-- PostgreSQL database dump complete
--

