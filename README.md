# DatingBot❤️
Telegram dating bot written on python/aiogram
- Using postgresql as database

# SQL tables structure

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
