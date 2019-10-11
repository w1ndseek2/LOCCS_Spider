from redis import StrictRedis
from data.config import REDIS_HOST, REDIS_PASS, REDIS_PORT
import os
#manage redis


class Manage_Redis:
    def __init__(self):
        self.tid = SPIDER_NAME  # loccs
        #connect to redis
        if REDIS_PASS:
            self.redis = StrictRedis(
                REDIS_HOST, REDIS_PORT, 0, REDIS_PASS, decode_responses=True)
        else:
            self.redis = StrictRedis(
                REDIS_HOST, REDIS_PORT, decode_responses=True)
        self.spiders = {}
        self.exited = 0
    
    def read_from_conf(self):
        file = os.path.abspath(os.path.dirname(__file__) + '/data/resolved_domain/test.txt')
        with open(file,'r') as f:
            for line in f.readlines():
                url = 'http://' + line.strip()
                self.add_todo(url)
        pass

    def get_todo(self):
        urls = self.redis.smembers(self.tid + "_todo")
        if urls:
            return urls
        else:
            return(None)

    def get_finish(self):
        urls = self.redis.smembers(self.tid + "_finish")
        if urls:
            return urls
        else:
            return(None)

    def get_timeout(self):
        urls = self.redis.smembers(self.tid + "_timeout")
        if urls:
            return urls
        else:
            return(None)

    def get_forbidden(self):
        urls = self.redis.smembers(self.tid + "_forbidden")
        if urls:
            return urls
        else:
            return(None)

    def get_login_form(self):
        urls = self.redis.smembers(self.tid + "_login_form")
        if urls:
            return urls
        else:
            return(None)
    
    def get_error(self):
        urls = self.redis.smembers(self.tid + "_error")
        #if empty
        if urls:
            return urls
        else:
            return(None)

    def get_todo_num(self):
        return self.redis.scard(self.tid + '_todo')

    def get_finish_num(self):
        return self.redis.scard(self.tid + '_finish')

    def get_timeout_num(self):
        return self.redis.scard(self.tid + '_timeout')

    def get_forbidden_num(self):
        return self.redis.scard(self.tid + '_forbidden')

    def get_login_form_num(self):
        return self.redis.scard(self.tid + '_login_form')

    def get_error_num(self):
        return self.redis.scard(self.tid + '_error')

    #add
    #sadd(key, value)
    def add_todo(self, url):
        ret = self.redis.sadd(self.tid + '_todo', url)
        if ret == 1:
            return 0, 'ADD TODO SUCCESS'
        else:
            return 1, 'URL EXISTS'

    def add_finish(self, url):
        ret = self.redis.sadd(self.tid + '_finish', url)
        if ret == 1:
            return 0, 'ADD FINISH SUCCESS'
        else:
            return 1, 'FINISH EXISTS'

    def add_timeout(self, url):
        ret = self.redis.sadd(self.tid + '_timeout', url)
        if ret == 1:
            return 0, 'ADD TIMEOUT SUCCESS'
        else:
            return 1, 'TIMEOUT EXISTS'

    def add_forbidden(self, url):
        ret = self.redis.sadd(self.tid + '_forbidden', url)
        if ret == 1:
            return 0, 'ADD FORBIDDEN SUCCESS'
        else:
            return 1, 'DISALLOW EXISTS'

    def add_login_form(self, url):
        ret = self.redis.sadd(self.tid + '_login_form', url)
        if ret == 1:
            return 0, 'ADD LOGIN FORM SUCCESS'
        else:
            return 1, 'LOGIN_FORM EXISTS'

    def add_error(self, url):
        ret = self.redis.sadd(self.tid + '_error', url)
        if ret == 1:
            return 0, 'ADD ERROR SUCCESS'
        else:
            return 1, 'ERROR EXISTS'

    #del
    #srem(key, value)
    def del_todo(self, url):
        ret = self.redis.srem(self.tid + '_todo', url)
        if ret == 1:
            return 0, 'REMOVE TODO SUCCESS'
        else:
            return 1, 'URL NOT EXISTS'

    def del_finish(self, url):
        ret = self.redis.srem(self.tid + '_finish', url)
        if ret == 1:
            return 0, 'REMOVE FINISH SUCCESS'
        else:
            return 1, 'URL NOT EXISTS'


    def del_timeout(self, url):
        ret = self.redis.srem(self.tid + '_timeout', url)
        if ret == 1:
            return 0, 'REMOVE TIMEOUT SUCCESS'
        else:
            return 1, 'URL NOT EXISTS'

    def del_forbidden(self, url):
        ret = self.redis.srem(self.tid + '_forbidden', url)
        if ret == 1:
            return 0, 'REMOVE FORBIDDEN SUCCESS'
        else:
            return 1, 'URL NOT EXISTS'

    def del_login_form(self, url):
        ret = self.redis.srem(self.tid + '_login_form', url)
        if ret == 1:
            return 0, 'REMOVE LOGIN FORM SUCCESS'
        else:
            return 1, 'URL NOT EXISTS'

    def del_error(self, url):
        ret = self.redis.srem(self.tid + '_error', url)
        if ret == 1:
            return 0, 'REMOVE ERROR SUCCESS'
        else:
            return 1, 'URL NOT EXISTS'

    def status(self):
        #print process status
        return 1, {
            'task': {
                'todo': self.get_todo_num(),
                'finish': self.get_finish_num(),
                'timeout': self.get_timeout_num(),
                'forbidden': self.get_forbidden_num(),
                'login_form': self.get_login_form_num(),
                'error':self.get_error_num()
            },
        }
