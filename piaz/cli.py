from piaz.config import V2RayConfig
from piaz.config.xui import XUIConfig
from piaz.options import parser


def main():
    opt = parser.parse_args()

    remote = opt.remote
    if remote == '' or remote == '-':
        remote = None

    config = None
    if opt.config == 'v2ray':
        config = V2RayConfig(remote)
    elif opt.config == 'xui':
        config = XUIConfig(remote)
    else:
        print(f"Unknown config: {opt.config}")
        return

    with config:
        config.apply()
