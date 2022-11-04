from piaz.utils import render_template
from .docker import DockerComposeConfig


class GostConfig(DockerComposeConfig):
    def __init__(self, remote, command):
        super().__init__(remote, 'ginuerzh/gost:latest', '.piaz/gost')
        self.command = command or '-L=:80'

    def get_compose(self):
        return render_template('gost/docker-compose.yml.j2', command=self.get_command())

    def get_command(self):
        return self.command
