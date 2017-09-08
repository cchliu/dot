"""
The central management of DDoS detection applications.

- Load DDoS detection applications.
- Route messages among detection applications.
"""
# Reference
# https://github.com/osrg/ryu/tree/master/ryu/base
#
import logging
import itertools
import inspect

from dot import utils
from dot.controller.handler import register_instance

LOG = logging.getLogger('dot.base.app_manager')
SERVICE_BRICKS = {}

def register_app(app):
    assert isinstance(app, DotApp)
    assert app.name not in SERVICE_BRICKS
    SERVICE_BRICKS[app.name] = app
    register_instance(app)

def unregister_app(app):
    SERVICE_BRICKS.pop(app.name)

class DotApp(object):
    """
    The base class for DDoS detection applications.
    DotApp subclasses are instantiated after app-manager loaded
    all requested application modules.
    __init__ should call DotApp.__init__ with the same arguments.
    It's illegal to send any events in __init__.

    The instance attribute 'name' is the name of the class used 
    for message routing among DDos detection applications.
    It's set to __class__.__name__ by DotApp.__init__.
    It's discouraged for subclasses to override this.

    """
    def __init__(self, *_args, **_kwargs):
        super(DotApp, self).__init__()
        self.name = self.__class__.__name__
        self.event_handlers = {}

class AppManager(object):
    # singleton
    _instance = None

    @staticmethod
    def get_instance():
        if not AppManager._instance:
            AppManager._instance = AppManager()
        return AppManager._instance

    def __init__(self):
        # key: app_cls_name, value: app_cls
        self.applications_cls = {}
        # key: app_name, value: app_cls object
        self.applications = {}
    
    def load_app(self, name):
        mod = utils.import_module(name)
        clses = inspect.getmembers(mod, lambda cls:(inspect.isclass(cls) and 
                                        issubclass(cls, DotApp) and 
                                        mod.__name__ == cls.__module__))
        if clses:
            return clses[0][1]
        return None

    def load_apps(self, app_lists):
        app_lists = [app for app in itertools.chain.from_iterable(app.split(',') for app in app_lists)]

        while len(app_lists)>0:
            app_cls_name = app_lists.pop(0)

            LOG.info('loading app %s', app_cls_name)

            cls = self.load_app(app_cls_name)
            if cls is None:
                continue
            self.applications_cls[app_cls_name] = cls
    
    def _instantiate(self, app_cls_name, cls, *args, **kwargs):
        # For now, only a single instance of a given module is instantiated.
        LOG.info('instantiating app %s of %s', app_cls_name, cls.__name__)
        if app_cls_name is not None:
            assert app_cls_name not in self.applications
        app = cls(*args, **kwargs)
        register_app(app)
        assert app.name not in self.applications
        self.applications[app.name] = app
        return app


    def instantiate_apps(self, *args, **kwargs):
        for app_cls_name, cls in self.applications_cls.items():
            self._instantiate(app_cls_name, cls, *args, **kwargs)

        


    
