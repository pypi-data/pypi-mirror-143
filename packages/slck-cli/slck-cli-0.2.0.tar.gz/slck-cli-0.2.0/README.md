# slck-cli: Simple cli tool to manage your slack workspace

![PyPI](https://img.shields.io/pypi/v/slck-cli?style=flat-square)
[![GitHub license](https://img.shields.io/github/license/joe-yama/slck-cli?style=flat-square)](https://github.com/joe-yama/slck-cli/blob/main/LICENSE)

## Basic Usage

```bash
# listing all users in workspace
$ slck user list
User(id='U031L3JNBKS', name='taro', real_name='Taro Yamada')
User(id='U036NS9S6HL', name='jiro', real_name='Jiro Tanaka')
User(id='U032SU3SKBS', name='hanako', real_name='Hanako Suzuki')

# user search by real_name (or name or id)
$ slck user find --real_name "Taro Yamada"
User(id='U031L3JNBKS', name='taro', real_name='Taro Yamada')

# channel list (filtered by prefix)
$ slck channel list --prefix general
Channel(id='C02AFAUOK33', name='general')

# most reacted post in the channel
$ slck message popular general
Message(message_type='message', user=User(id='U031L3JNBKS', name='taro', real_name='Taro Yamada'), channel=Channel(id='C02AFAUOK33', name='general'), ts='1647648476.156199', text='テスト', num_reply=0, num_replyuser=0, num_reaction=3, permalink='https://foo.slack.com/archives/C02AFAUOK33/p23471289471123')
```

## Installation

```bash
pip install slck-cli
```

## License

This software is released under the MIT License, see LICENSE.
