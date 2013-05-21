import getpass
import redis

'''
Basic Usage: 
    conf = Config('namespace')
    conf.setConf('keyname', 'value')
    conf.getConf('keyname')

    questions = []
    questions.append({'key':'mongodb_host','question':"What is mongodb's host?", 'keep_default':True})
    questions.append({'key':'mongodb_port','question':"What is mongodb's port?", 'default':27017})
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
            questions.append({'key':'mongodb_host','question':"What is mongodb's host?", 'keep_default':True})
            questions.append({'key':'mongodb_port','question':"What is mongodb's port?", 'default':27017})
            questions.append({'key':'mongodb_pass','question':"What is mongodb's password?", 'is_password':True})
            conf.configureEnvironment(questions)
        '''
        for question_data in setup_info:
            # Set vars
            key = question_data['key']
            is_password = False
            if question_data.has_key('is_password'):
                is_password = question_data['is_password']
            keep_default = False
            if question_data.has_key('keep_default'):
                keep_default = question_data['keep_default']
            default = False
            if question_data.has_key('default'):
                default = question_data['default']
            question = question_data['question']
            
            # Include default values on question
            if keep_default:
                old_value = ''
                if is_password:
                    old_value = 'OLD PASSWORD'
                else:
                    old_value = self.getConf(key)
                question += ' (DEFAULT: '+old_value+')'
            elif default:
                question += ' (DEFAULT: '+str(default)+')'
            
            # Is Password
            if is_password:
                value = getpass.getpass(question+": ")
            else:
                value = raw_input(question+": ")
            
            # Set Default Value
            if not value:
                if keep_default:
                    continue
                elif default:
                    value = default
            self.setConf(key, value)
        return

    def getEnvironmentConfig(self):
        keys = self.conn.keys(self.namespace+'.*')
        conf = {}
        for key in keys:
            conf[key.replace(self.namespace+'.', '')] = self.conn.get(key)
        return conf