import traceback, types, sys
import win32con, win32event, win32process, win32security
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon

def isUserAdmin():
    try:
        adminSid = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid, None)
        return win32security.CheckTokenMembership(None, adminSid)
    except:
        traceback.print_exc()
        return False

def test():
    rc = 0
    if not isUserAdmin():
        rc = runAsAdmin()
    else:
        rc = 0
    return rc

def runAsAdmin(cmdLine=None, wait=True):
    python_exe = sys.executable
    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType,types.ListType):
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'
    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']    
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
    else:
        rc = None
    return rc