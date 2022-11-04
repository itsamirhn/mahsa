from piaz.utils import render_template
from .docker import DockerComposeConfig


class XUIConfig(DockerComposeConfig):
    def __init__(self, **kwargs):
        super().__init__(image='x-ui/x-ui:latest', directory='.piaz/xui', **kwargs)

    def get_compose(self):
        return render_template('xui/docker-compose.yml.j2', image=self.image)

    def apply(self):
        super().apply()
        print(f"XUI is running at http://{self.host}:54321")
        print(f"Username: admin")
        print(f"Password: admin")
