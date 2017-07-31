from .helpers import ResourceBase, IterableResource
from .errors import ok_or_error, response_or_error
from .compat import update_doc
from .helpers import Nested, StringFormater

class StashKey(StringFormater):
    def __init__(self,key,permission):
        self.key=key
        self.permission=permission
    
class ReposKey(ResourceBase):
    def __init__(self, key,url, client, parent):
        super(ReposKey, self).__init__(url, client, parent)
        self._key = key
        self._url=url
        
    @response_or_error
    def _keys(self):
        return self._client.get(self.url())

    def all(self):
        raw=self._keys()
        ret=[]
        for data in raw["values"]:
            key=data["key"]["text"]
            permission=data["permission"]
            ret.append(StashKey(key,permission))
        return ret

class Repos(ResourceBase):
    def __init__(self,url, client, parent):
        super(Repos, self).__init__(url, client, parent)
        self._url=url
        
    def __getitem__(self, item):
        return ReposKey(item, self.url(item)+"/ssh", self._client, self)

class ProjectKey(ResourceBase):
    repos = Nested(Repos)
    def __init__(self, key,url, client, parent):
        super(ProjectKey, self).__init__(url, client, parent)
        self._key = key
        self._url=url

    @response_or_error
    def _keys(self):
        return self._client.get(self.url("ssh"))

    def all(self):
        raw=self._keys()
        ret=[]
        for data in raw["values"]:
            key=data["key"]["text"]
            permission=data["permission"]
            ret.append(StashKey(key,permission))
        return ret


class ProjectKeys(ResourceBase):
    
    def __init__(self, url, client, parent):
        super(ProjectKeys, self).__init__(url, client, parent)
        self._url = 'keys/1.0/projects'

    def __getitem__(self, item):
        return ProjectKey(item, self.url(item), self._client, self)