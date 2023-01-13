import win32event

m = win32event.CreateMutex(None, False, 'MyMutex')
m = win32event.OpenMutex(win32event.SYNCHRONIZE, False, 'MyMutex')
r = win32event.WaitForSingleObject(m, 100)
r = win32event. WaitForSingleObject(m, -1)
win32event.ReleaseMutex(m)