# Define NewFileEvent subclass

from dot.controller import event

class NewFileEvent(event.EventBase):
    def __init__(self, filename):
        super(TestEvent, self).__init__()
        self.filename = filename

