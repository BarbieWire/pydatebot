# DatingBot❤️
Telegram dating bot written on python/aiogram
1. Using postgresql as database
2. Heroku as deployment service for application

> ### ___P.S Heroku was used to deploy both of them___
> - database and application 

# Usage:
*Worker: main.py*
- Download side-packages from requirements.txt
- Rename ___example.env___ to ___.env___
- Change all global variables in ___.env___ file

# SQL tables structure
**Table "users"**
> place for storing personal data of users
```sql
CREATE TABLE users (
    chat_id integer NOT NULL,
    photo character varying,
    city character varying,
    gender character varying,
    name character varying,
    preference character varying,
    about character varying,
    age integer,
    active character varying,
    CONSTRAINT users_pkey PRIMARY KEY (chat_id)
)
```
**Table "likes"**
> centralized table of likes
```sql
CREATE TABLE likes (
    id integer NOT NULL,
    liker character varying(30),
    liked character varying(30),
    mutual character varying(30),
    CONSTRAINT likes_pkey PRIMARY KEY (id)
)
```
### __Don't forget to repo's support author with your star⭐__
