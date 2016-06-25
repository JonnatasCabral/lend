from io import BytesIO
from docker import Client
from core.constants import dockerfile


class Docker(object):
	
	cli = None
	image = None
	container = None
	
	def __init__(self):
		self.cli = Client(base_url='unix://var/run/docker.sock')
		self.container = self.container_create()
		self.image = self.create_image(dockerfile)

	def create_image(self, dockerfile, tag='python/lend', rm=True):
	    f = BytesIO(dockerfile)

	    response = [line for line in self.cli.build(
	        fileobj=f, rm=rm, tag=tag
	    )]
	    return response


	def container_create(self):
		container = self.cli.create_container(
		    image='python/lend',
		    stdin_open=True,
		    volumes={"/tmp/codes": {}},
		    tty=True,
		    command='/bin/sh',
		)
		return container

	def container_up(self, container):
		"""
			Recebe um dict com Id do container e roda o container
		"""
		return self.cli.start(container,  binds=["/tmp/codes:/home/codes"])

	def container_down(self, container):

		return self.cli.stop(container)

	def container_run_command(self, container, command):
		"""
			Recebe um container e um comando, o ultimo no formato de str. Retorna
			o um dict com a chave para essa execução.

		"""
		r = self.cli.exec_create(container, command)
		return self.container_response(r)

	def container_response(self, exec_create):
		"""
			Recebe um dict com a chave da execução de um exec_create
			e retorna o resultado que o bash retornou.
		"""
		return self.cli.exec_start(exec_create)
