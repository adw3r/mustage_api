create `.env` file for environment variables using `example.env`

### How to run
~~~bash
docker-compose up --build -d
docker-compose exec api uv run alembic upgrade heads
~~~
