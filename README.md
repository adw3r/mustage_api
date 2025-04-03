create `.env` file for environment variables using `example.env`

### Boot up
~~~bash
docker-compose up --build -d && docker-compose exec api uv run alembic upgrade heads
~~~
