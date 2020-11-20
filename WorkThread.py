import threading
import time
import ctypes

class WorkThread(threading.Thread):
    def __init__(self, target=None, *args, **kwargs):
        super(WorkThread, self).__init__(target=target, *args, **kwargs)

    def stop(self):
        try:
            self.raise_exception()
        except Exception as e:
            print(e)

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self: 
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')