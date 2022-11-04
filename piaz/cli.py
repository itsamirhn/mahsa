from piaz.config import V2RayConfig, GostConfig, XUIConfig
from piaz.options import parser


def main():
    opt = parser.parse_args()

    remote = opt.remote
    if remote == '' or remote == '-':
        remote = None

    if opt.tool == 'v2ray':
        config = V2RayConfig(remote)
    elif opt.tool == 'xui':
        config = XUIConfig(remote)
    elif opt.tool == 'gost':
        config = GostConfig(remote, opt.command)
    else:
        print(f"Unknown tool: {opt.tool}")
        return

    with config:
        config.apply()
