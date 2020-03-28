dev.makemigrations:
	docker exec -it -w /src/backend/ com.oscar.store python3 manage.py makemigrations
dev.collectstatic :
	docker exec -it -w /src/backend/ com.oscar.store python3 manage.py collectstatic_schemas --noinput --schema=$(schema)
dev.migrate:
	docker exec -it -w /src/backend/ com.oscar.store python3 manage.py migrate_schemas
dev.oscar_populate_countries:
	docker exec -it -w /src/backend/ com.oscar.store python3 manage.py oscar_populate_countries
dev.requirements:
	docker exec -it -w /src/backend/ com.oscar.store pip3 install -r requirements
dev.ping.psql.primzel.com:
	 docker exec -it -w /src/backend/ com.oscar.store ping psql.primzel.com
dev.ping.redis.oscar.com:
	 docker exec -it -w /src/backend/ com.oscar.store ping redis.oscar.com
dev.celery.beat.shell:
	docker exec -it -w /src/backend/ com.oscar.celery_beat bash
dev.celery.worker.shell:
	docker exec -it -w /src/backend/ com.oscar.celery_worker bash
dev.web.shell:
	docker exec -it -w /src/backend/ com.oscar.store bash
dev.redis.shell:
	docker exec -it -w /src/backend/ com.oscar.redis bash
dev.postgres.shell:
	docker exec -it com.primzel.psql psql -U postgres