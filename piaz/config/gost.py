from piaz.utils import render_template
from .docker import DockerComposeConfig


class GostConfig(DockerComposeConfig):
    DEFAULT_COMMAND = '-L=relay+tls://piaz:piazche@:6121'

    def __init__(self, command, **kwargs):
        super().__init__(image='ginuerzh/gost:latest', directory='.piaz/gost', **kwargs)
        self.command = command or self.DEFAULT_COMMAND

    def get_compose(self):
        return render_template('gost/docker-compose.yml.j2', command=self.command, image=self.image)

    def apply(self):
        super().apply()
        print('Gost is running with command: {}'.format(self.command))
