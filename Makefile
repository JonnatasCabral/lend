clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;

clean.migrations:
	@git ls-files | grep migrations > skip_migrations
	@echo 'Migrações a serem removidas:'
	@find . -path "*/migrations/*.py*" | grep -vFf skip_migrations
	@find . -path "*/migrations/*.py*" | grep -vFf skip_migrations | xargs rm
	@echo 'Migrações removidas com sucesso!'
	@rm skip_migrations

serve:
	@python manage.py runserver

migrations:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

shell:
	@iprofile django

oauth:
	@python manage.py oauth

super:
	@python manage.py createsuperuser

static:
	@python manage.py collectstatic

new: migrations migrate super oauth

sync: migrations migrate oauth
