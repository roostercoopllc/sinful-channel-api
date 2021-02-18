from requests.api import request
import yaml

# Don't know if we will use this or not
class ChannelRewardsHandler(object):
    def __init__(self, clientId=None, clientSecret=None, from_config=False):
        if from_config:
            with open('../channel-rewards.yml', 'r', encoding='utf-8') as fi:
                config = yaml.load(fi, Loader=yaml.SafeLoader)
                self.clientId = config['clientId']
                self.clientSecrets = config['clientSecrets']
        else:
            self.clientId = clientId
            self.clientSecrets = clientSecret
        self.token = None