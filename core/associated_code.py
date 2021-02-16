import yaml

with open('channel-rewards.yml', 'r', encoding='utf-8') as fi:
    config = yaml.load(fi, Loader=yaml.SafeLoader)

