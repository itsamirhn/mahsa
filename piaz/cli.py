from piaz.config import V2RayConfig, GostConfig, XUIConfig
from piaz.options import parser


def main():
    opt = parser.parse_args()

    tools = {
        'v2ray': V2RayConfig,
        'gost': GostConfig,
        'xui': XUIConfig,
    }
    config = tools[opt.tool](**vars(opt))

    with config:
        config.apply()
