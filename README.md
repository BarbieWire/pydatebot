# DatingBot❤️
Telegram dating bot written on python/aiogram
- Using postgresql as database

# SQL tables structure

**Table "likes"**
```sql
CREATE TABLE IF NOT EXISTS public.likes
(
    id integer NOT NULL DEFAULT nextval('likes_id_seq'::regclass),
    liker character varying COLLATE pg_catalog."default",
    liked character varying COLLATE pg_catalog."default",
    mutual character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT likes_pkey PRIMARY KEY (id)
)
```
**Table "users"**
```sql
CREATE TABLE IF NOT EXISTS public.users
(
    chat_id integer NOT NULL,
    photo character varying COLLATE pg_catalog."default",
    city character varying COLLATE pg_catalog."default",
    gender character varying COLLATE pg_catalog."default",
    name character varying COLLATE pg_catalog."default",
    preference character varying COLLATE pg_catalog."default",
    about character varying COLLATE pg_catalog."default",
    age integer,
    active character varying COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (chat_id)
)
```
