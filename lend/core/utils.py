from io import BytesIO
from docker import Client
from core.constants import dockerfile
from core.constants import base_url

def create_image(dockerfile, base_url, tag='new_image',rm=True):
	f = BytesIO(dockerfile.encode('utf-8'))
	cli = Client(base_url=base_url)

	response = [line for line in cli.build(
	    fileobj=f, rm=rm, tag=tag
	)]
	return response
	