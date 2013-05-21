redisconf
=========

Basic module to store environment configuration on redis

# Installation

    $ pip install git+git@github.com:brunogfranca/redisconf.git

# Basic Usage

    from redisconf.config import Config

    conf = Config('namespace')
    conf.setConf('keyname', 'value')
    conf.getConf('keyname')

    questions = []
    questions.append({'key':'mongodb_host','question':"mongodb's host?"})
    questions.append({'key':'mongodb_port','question':"mongodb's port?", 'default':27017})
    questions.append({'key':'mongodb_pass','question':"mongodb's password?", 'is_password':True})
    conf.configureEnvironment(questions)

    conf.getEnvironmentConfig()