import unittest
import mock

from . import config


class Test(unittest.TestCase):

    @mock.patch('redis.StrictRedis')
    def test_config_instance_should_be_works(self, strict_redis):
        config.Config('namespace')
        strict_redis.assert_called_with()
        config.Config('another_namespace', host='host-doidao.dev')
        strict_redis.assert_called_with(host='host-doidao.dev')
