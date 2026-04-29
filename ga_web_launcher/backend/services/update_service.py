"""Update Service - 代码更新服务"""
from decorators.repo_decorator import RepoDecorator
from core.paths import GA_ROOT_DEFAULT

class UpdateService:
    def __init__(self, ga_root=None):
        self.repo = RepoDecorator(ga_root or GA_ROOT_DEFAULT)
    
    def get_status(self):
        return self.repo.get_status()
    
    def check_update(self):
        return self.repo.check_update()
    
    def pull_latest(self):
        return self.repo.pull_latest()
