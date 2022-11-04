from piaz.utils import render_template
from .docker import DockerComposeConfig


class XUIConfig(DockerComposeConfig):
    def __init__(self, remote):
        super().__init__(remote, 'x-ui/x-ui:latest', '.piaz/xui')

    def get_compose(self):
        return render_template('xui/docker-compose.yml.j2')

    def apply(self):
        super().apply()
        print(f"XUI is running at http://{self.host}:54321")
        print(f"Username: admin")
        print(f"Password: admin")
