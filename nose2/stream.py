from nose2.events import BeforeReportEvent


class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self, stream, session):
        self.stream = stream
        self.session = session

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def write(self, arg, **kwargs):
        event = BeforeReportEvent(self, arg, **kwargs)
        self.session.hooks.reportBeforeReport(event)

        if not event.handled:
            self.stream.write(arg)

    def writeln(self, arg=None, **kwargs):
        event = BeforeReportEvent(self, arg, **kwargs)
        self.session.hooks.reportBeforeReport(event)

        if not event.handled:
            if arg:
                self.stream.write(arg)
        self.stream.write('\n') # text-mode streams translate to \r\n if needed
