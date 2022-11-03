import base64
import json
import os
import uuid
from pathlib import Path

import qrcode
from jinja2 import Template

from .docker import DockerConfig


class V2RayConfig(DockerConfig):

    def __init__(self, remote, port=80, path='/ws'):
        super().__init__(remote, 'ghcr.io/getimages/v2fly-core:v4.45.2')
        self.config = {
            "port": port,
            "secret": str(uuid.uuid4()),
            "path": path
        }

    def render_template(self, name):
        with open(Path(__file__).parent.parent / 'templates' / 'v2ray' / name) as file_:
            template = Template(file_.read())
        print(f"Rendering template {name}")
        return template.render(**self.config, host=self.host)

    def prepare_template(self, name):
        with open(name, "w") as file_:
            file_.write(self.render_template(f'{name}.j2'))
        print(f"Uploading {name}")
        self.sftp.put(name, f".piaz/v2ray/{name}")
        os.remove(name)

    def prepare(self):
        super().prepare()
        if not self.file_exists('.piaz/v2ray'):
            print("Creating .piaz/v2ray directory")
            self.sftp.mkdir('.piaz/v2ray')
        if not self.file_exists(f".piaz/v2ray/config.json"):
            self.prepare_template('config.json')
        if not self.file_exists(f".piaz/v2ray/docker-compose.yml"):
            self.prepare_template('docker-compose.yml')

    def get_link(self):
        dic = dict(id=self.config['secret'], aid="0", v="2", tls="", add=self.host, port=self.config["port"], type="",
                   net="ws", path=self.config['path'], host="", ps=f"{self.host} (Created by piaz)")
        return "vmess://" + base64.b64encode(json.dumps(dic, sort_keys=True).encode('utf-8')).decode()

    def apply(self):
        super().apply()
        _, stdout, stderr = self.ssh.exec_command('docker compose -f .piaz/v2ray/docker-compose.yml up -d')
        print(stdout.read().decode())
        print(stderr.read().decode())
        link = self.get_link()
        qr = qrcode.QRCode()
        qr.add_data(link)
        qr.print_ascii()
        print(link)
