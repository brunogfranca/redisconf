import getpass
import redis

'''
Basic Usage: 
    conf = Config('namespace')
    conf.setConf('keyname', 'value')
    conf.getConf('keyname')

    questions = []
    questions.append({'key':'mongodb_host','question':"What is mongodb's host?"})
    questions.append({'key':'mongodb_port','question':"What is mongodb's port?"})
    questions.append({'key':'mongodb_pass','question':"What is mongodb's password?", 'is_password':True})
    conf.configureEnvironment(questions)

    conf.getEnvironmentConfig()
'''
class Config(object):
    def __init__(self, namespace):
        self.namespace = namespace
        self.conn = redis.StrictRedis(host='localhost', port=6379, db=0)

    def setConf(self, key, value):
        return self.conn.set(self.namespace+'.'+key, value)

    def getConf(self, key):
        return self.conn.get(self.namespace+'.'+key)

    def configureEnvironment(self, setup_info):
        '''
        Usage: 
            questions = []
            questions.append({'key':'mongodb_host',"question':'What is mongodb's host?"})
            questions.append({'key':'mongodb_port',"question':'What is mongodb's port?", 'default':27017})
            questions.append({'key':'mongodb_pass',"question':'What is mongodb's password?", 'is_password':True})
            conf.configureEnvironment(questions)
        '''
        for question_data in setup_info:
            if question_data.has_key('is_password') and question_data['is_password']:
                value = getpass.getpass(question_data['question']+": ")
            else:
                value = raw_input(question_data['question']+": ")
            if not value:
                if question_data.has_key('default') and question_data['default']:
                    value = question_data['default']
            self.setConf(question_data['key'], value)
        return

    def getEnvironmentConfig(self):
        keys = self.conn.keys(self.namespace+'.*')
        conf = {}
        for key in keys:
            conf[key] = self.conn.get(key)
        return conf