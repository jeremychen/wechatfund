# -*- coding: utf-8 -*-

try:
     import cPickle as pickle
except ImportError:
    import pickle
import sae.kvdb

class SaeDb(object):
    ''' 封装SAE kvDB,key为用户id,value为订阅的基金代码列表 '''
    def __init__(self, user):
        self.user = user
        self.kv = sae.kvdb.KVClient()
    def set(self, data):
        return self.kv.set(self.user, self._tostr(data))
    def get(self):
        sdata = self.kv.get(self.user)
        if sdata:
            return self._tolist(self.kv.get(self.user))
        return sdata
    def delete(self):
        return self.kv.delete(self.user)
    def append(self, iterm):
        sdata = self.kv.get(self.user)
        if sdata:
            data = self._tolist(sdata)
            if not iterm in data:
                data.append(iterm)
                return self.kv.replace(self.user, self._tostr(data))
        else:
            data = [iterm]
            return self.kv.set(self.user, self._tostr(data))
    def remove(self, iterm):
        sdata = self.kv.get(self.user)
        if sdata:
            data = self._tolist(sdata)
            if iterm in data:
                data.remove(iterm)
                self.kv.replace(self.user, self._tostr(data))
    def len(self):
        if self.kv.get(self.user):
            return len(self._tolist(self.kv.get(self.user)))
        else: return 0
    def isempty(self):
        return not self.kv.get()
    def _tostr(self, data):
        return pickle.dumps(data)
    def _tolist(self, data):
        return pickle.loads(data)
        
    