'''
Peng Sun
agentUtil.py
utility
'''

import inspect
import multiprocessing
#import logging

_LAZY_M_ENABLED_ = True

_MAN_DEBUG_ = False
_SND_DEBUG_ = False
_RCV_DEBUG_ = False
_CONTROL_DEBUG_ = False
_DIRSERVICE_DEBUG_ = False
_LIB_DEBUG_ = False
_JOB_BUILD_DEBUG_ = False
_SCH_DEBUG_ = False
_CONN_DEBUG_ = False
_PROC_DEBUG_ = False

_debugFlags = {'manager' : _MAN_DEBUG_,
               'sndMod'  : _SND_DEBUG_,
               'rcvMod'  : _RCV_DEBUG_,
               'control' : _CONTROL_DEBUG_,
               'dir'     : _DIRSERVICE_DEBUG_,
               'lib'     : _LIB_DEBUG_,
               'job'     : _JOB_BUILD_DEBUG_,
               'schedule': _SCH_DEBUG_,
               'conn'    : _CONN_DEBUG_,
               'proc'    : _PROC_DEBUG_}

_loggingLock = multiprocessing.Lock()

_logFileName = None
_logs = []

IPCType = {'NewSourceJob' : 1,
           'UpdateSourceJob': 2,
           'InstallSocketCriteria': 3,
           'DeleteSocketCriteria': 4,
           'NewSocket': 5,
           'DeleteSocket': 6,
           'AddSkToJobFlow': 7,
           'RemoveSkFromJobFlow': 8}

def IsLazyTableEnabled():
    return _LAZY_M_ENABLED_

def debugLog(module, *args):
    flag = _debugFlags.get(module, False)
    if flag:
        _loggingLock.acquire()
        _, fileName, lineNumber, _, _, _ = inspect.stack()[1]
        tmp = fileName.split('/')
        fileName = tmp[len(tmp) - 1]
        print '\nDEBUG ' + fileName + ', L' + str(lineNumber) + ': '
        for i in range(0, len(args)):
            print args[i]
        print '\n'
        _loggingLock.release()

def composeKey(jobId, flowId):
    return '{0}@{1}'.format(jobId, flowId)

def decomposeKey(key):
    [jobId, flowId] = key.split('@')
    return (int(jobId), int(flowId))

def keyContainJobId(key, jobId):
    [keyJobId, keyFlowId] = key.split('@')
    return (keyJobId == str(jobId))

def middleJobKeyContainJobIdAndLevel(key, jobId, level):
    [keyJobId, _, keyLevel] = key.split('@')
    return (keyJobId == str(jobId)) and (keyLevel == str(level))

def composeMiddleJobKey(jobId, flowId, level):
    return '{0}@{1}@{2}'.format(jobId, flowId, level)

def SetLogFileName(logFileName):
    global _logFileName
    _logFileName = logFileName

def EvalLog(info):
    #print 'EvalLog: {0}'.format(info)
    global _logs
    _logs.append(info)

def WriteLogs():
    global _logFileName
    global _logs
    if _logFileName and _logs:
        output = open(_logFileName, 'a')
        for log in _logs:
            print >>output, log
        output.close()
        del _logs[:]
    