import os

from .base import Config


class DockerInstallConfig(Config):

    def install(self):
        print("Installing Docker")
        self.ssh.exec_command('curl https://get.docker.com | sh')
        self.ssh.exec_command('sudo usermod -aG docker $USER')

    def is_installed(self):
        stdin, stdout, stderr = self.ssh.exec_command('docker --version')
        return stdout.read().decode().startswith('Docker version')

    def prepare(self):
        super().prepare()
        if not self.is_installed():
            self.install()


class DockerPullConfig(DockerInstallConfig):

    def __init__(self, remote, image):
        super().__init__(remote)
        self.image = image

    def pull(self):
        print(f"Pulling image {self.image}")
        self.ssh.exec_command(f'docker pull {self.image}')

    def has_pulled(self):
        image_name = self.image.split(':')[0]
        _, stdout, _ = self.ssh.exec_command(f'docker images {image_name}')
        return image_name in stdout.read().decode()

    def prepare(self):
        super().prepare()
        if not self.has_pulled():
            self.pull()


class DockerComposeConfig(DockerPullConfig):
    def __init__(self, remote, image, directory):
        super().__init__(remote, image)
        self.directory = directory

    def get_compose(self):
        raise NotImplementedError

    def prepare_compose(self):
        with open("docker-compose.yml", "w") as file_:
            file_.write(self.get_compose())
        print(f"Uploading {self.directory}/docker-compose.yml")
        self.sftp.put("docker-compose.yml", f'{self.directory}/docker-compose.yml')
        os.remove("docker-compose.yml")

    def prepare(self):
        super().prepare()
        if not self.file_exists(self.directory):
            print(f"Creating {self.directory} directory")
            self.sftp.mkdir(self.directory)
        if not self.file_exists(f'{self.directory}/docker-compose.yml'):
            self.prepare_compose()

    def compose_up(self):
        _, stdout, stderr = self.ssh.exec_command(f'docker compose -f {self.directory}/docker-compose.yml up -d')
        print(stdout.read().decode())
        print(stderr.read().decode())

    def apply(self):
        super().apply()
        self.compose_up()

