import getpass
import redis

'''
Basic Usage: 
    conf = Config('namespace')
    conf.setConf('keyname', 'value')
    conf.getConf('keyname')

    questions = []
    questions.append({'key':'mongodb_host','question':"mongodb's host"})
    questions.append({'key':'mongodb_port','question':"mongodb's port", 'default':27017})
    questions.append({'key':'mongodb_pass','question':"mongodb's password", 'is_password':True})
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
            questions.append({'key':'mongodb_host','question':"mongodb's host"})
            questions.append({'key':'mongodb_port','question':"mongodb's port", 'default':27017})
            questions.append({'key':'mongodb_pass','question':"mongodb's password", 'is_password':True})
            conf.configureEnvironment(questions)
        '''
        for question_data in setup_info:
            # Set vars
            key = question_data['key']
            is_password = False
            if question_data.has_key('is_password'):
                is_password = question_data['is_password']
            default = False
            if question_data.has_key('default'):
                default = question_data['default']
            question = question_data['question']
            
            # Check if the user wants to change the current value
            change = 'Y'
            old_value = self.getConf(key)
            if old_value:
                change_question = 'Do you want to change the current value for '+question+'?'
                if is_password:
                    old_value = 'OLD PASSWORD'
                change_question += ' ('+old_value+')'
                change_question += ' [y/N]'
                change = raw_input(change_question)
                if change == '':
                    change = 'N'
                while change.lower() not in ['y', 'n']:
                    change = raw_input(change_question)
                    if change == '':
                        change = 'N'

            value = ''
            if change.lower() == 'y':
                # Is Password
                if is_password:
                    value = getpass.getpass(question+": ")
                else:
                    if default:
                        question += ' ('+str(default)+')'
                    value = raw_input(question+": ")
            
                # Set Default Value
                if not value:
                    if default:
                        value = default
                self.setConf(key, value)
        return

    def getEnvironmentConfig(self):
        keys = self.conn.keys(self.namespace+'.*')
        conf = {}
        for key in keys:
            conf[key.replace(self.namespace+'.', '')] = self.conn.get(key)
        return conf