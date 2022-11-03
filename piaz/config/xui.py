from pathlib import Path

from .docker import DockerConfig


class XUIConfig(DockerConfig):
    def __init__(self, remote):
        super().__init__(remote, 'enwaiax/x-ui:latest')

    def prepare(self):
        super().prepare()
        if not self.file_exists('.piaz/x-ui'):
            print("Creating x-ui directory")
            self.sftp.mkdir('.piaz/x-ui')
        if not self.file_exists('.piaz/x-ui/docker-compose.yml'):
            self.sftp.put(Path(__file__).parent.parent / 'templates' / 'x-ui' / 'docker-compose.yml',
                          '.piaz/x-ui/docker-compose.yml')

    def apply(self):
        super().apply()
        _, stdout, stderr = self.ssh.exec_command('docker compose -f .piaz/x-ui/docker-compose.yml up -d')
        print(stdout.read().decode())
        print(stderr.read().decode())
        print(f"XUI is running at http://{self.host}:54321")
        print(f"Username: admin")
        print(f"Password: admin")
