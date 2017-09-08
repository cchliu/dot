# Test Application Module
from dot.base import app_manager

class Test(app_manager.DotApp):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
