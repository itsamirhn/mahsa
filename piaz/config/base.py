import paramiko

from piaz.utils import parse_remote


class Config:

    def __init__(self, remote):
        self.username, self.password, self.port, self.host = parse_remote(remote)
        self.port = self.port or 22
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")
        self.ssh.connect(self.host, username=self.username, password=self.password, port=self.port or 22, timeout=10)
        print("Connected")
        print("Opening SFTP")
        self.sftp = self.ssh.open_sftp()

    def close(self):
        self.sftp.close()
        self.ssh.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def file_exists(self, path):
        try:
            self.sftp.stat(path)
            return True
        except IOError:
            return False

    def prepare(self):
        if not self.file_exists('.piaz'):
            print("Creating .piaz directory")
            self.sftp.mkdir('.piaz')

    def apply(self):
        self.prepare()
