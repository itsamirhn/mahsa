from piaz.utils import render_template
from .docker import DockerComposeConfig


class GostConfig(DockerComposeConfig):
    def __init__(self, command, **kwargs):
        super().__init__(image='ginuerzh/gost:latest', directory='.piaz/gost', **kwargs)
        self.command = command or '-L=:80'

    def get_compose(self):
        return render_template('gost/docker-compose.yml.j2', command=self.command)

    def apply(self):
        super().apply()
        print('Gost is running with command: {}'.format(self.command))
