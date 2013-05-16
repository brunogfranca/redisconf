redisconf
=========

Basic module to store environment configuration on redis

# Installation

Execute the following commands:

    $ cd DESTINATION-FOLDER
    $ git clone https://github.com/brunogfranca/redisconf.git
    $ cd redisconf
    # python setup.py develop

# Basic Usage

    from redisconf.config import Config

    conf = Config('namespace')
    conf.setConf('keyname', 'value')
    conf.getConf('keyname')

    questions = []
    questions.append({'key':'mongodb_host','question':"What is mongodb's host?"})
    questions.append({'key':'mongodb_port','question':"What is mongodb's port? (27017)", 'default':27017})
    questions.append({'key':'mongodb_pass','question':"What is mongodb's password?", 'is_password':True})
    conf.configureEnvironment(questions)

    conf.getEnvironmentConfig()