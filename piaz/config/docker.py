from .base import Config


class DockerConfig(Config):
    def __init__(self, remote, image):
        super().__init__(remote)
        self.image = image

    def install(self):
        print("Installing Docker")
        self.ssh.exec_command('curl https://get.docker.com | sh')
        self.ssh.exec_command('sudo usermod -aG docker $USER')

    def is_installed(self):
        stdin, stdout, stderr = self.ssh.exec_command('docker --version')
        return stdout.read().decode().startswith('Docker version')

    def pull(self):
        print(f"Pulling image {self.image}")
        self.ssh.exec_command(f'docker pull {self.image}')

    def has_pulled(self):
        image_name = self.image.split(':')[0]
        _, stdout, _ = self.ssh.exec_command(f'docker images {image_name}')
        return image_name in stdout.read().decode()

    def prepare(self):
        super().prepare()
        if not self.is_installed():
            self.install()
        if not self.has_pulled():
            self.pull()

