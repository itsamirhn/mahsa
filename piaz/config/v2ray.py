import base64
import json
import os
import uuid

import qrcode

from .docker import DockerComposeConfig
from piaz.utils import render_template


class V2RayConfig(DockerComposeConfig):

    def __init__(self, ws_port=80, ws_path='/ws', **kwargs):
        super().__init__(image='ghcr.io/getimages/v2fly-core:v4.45.2', directory='.piaz/v2ray', **kwargs)
        self.config = {
            "port": ws_port,
            "secret": str(uuid.uuid4()),
            "path": ws_path
        }

    def get_compose(self):
        return render_template('v2ray/docker-compose.yml.j2', **self.config)

    def get_config(self):
        return render_template('v2ray/config.json.j2', **self.config)

    def prepare_config(self):
        with open("config.json", "w") as f:
            f.write(self.get_config())
        self.sftp.put("config.json", ".piaz/v2ray/config.json")
        os.remove("config.json")

    def prepare(self):
        super().prepare()
        if not self.file_exists(f".piaz/v2ray/config.json"):
            self.prepare_config()

    def get_link(self):
        dic = dict(id=self.config['secret'], aid="0", v="2", tls="", add=self.host, port=self.config["port"], type="",
                   net="ws", path=self.config['path'], host="", ps=f"{self.host} (Created by piaz)")
        return "vmess://" + base64.b64encode(json.dumps(dic, sort_keys=True).encode('utf-8')).decode()

    def apply(self):
        super().apply()
        link = self.get_link()
        qr = qrcode.QRCode()
        qr.add_data(link)
        qr.print_ascii()
        print(link)
