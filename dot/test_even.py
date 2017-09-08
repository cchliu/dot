# Define TestEvent subclass

from dot.controller from event

class TestEvent(event.EventBase):
    def __init__(self, msg):
        super(TestEvent, self).__init__()
