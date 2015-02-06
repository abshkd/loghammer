'''www.webmastersupport.com'''
__author__ = 'abhishek.dujari@gmail.com'

HOST = ''
PORT = 9999
TMPFILE = 'log.tmp'
BLOCK_FILE_SIZE = 33554432
DEBUG = 'debug.log'
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer
import time, re, math, os, datetime, errno




def mkdir_p(path):
    try:
        os.makedirs(path)

    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
    return path

severity = ['emerg', 'alert', 'crit', 'err', 'warn', 'notice', 'info', 'debug', ]

facility = ['kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news',
            'uucp', 'cron', 'authpriv', 'ftp', 'ntp', 'audit', 'alert', 'at', 'local0',
            'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7',]
fs_match = re.compile("<(.+)>(.*)", re.I)
#class Echo(DatagramProtocol):
#
#    def datagramReceived(self, data, (host, port)):
#        print "%r" % (data)
#    #        self.transport.write(data, (host, port))

#for TCP use by writing new protocol
#class LoggingProtocol(LineReceiver):
#
#    def lineReceived(self, line):
#        self.factory.fp.write(line+'\n')
#
#
#class LogfileFactory(Factory):
#
#    protocol = LoggingProtocol
#
#    def __init__(self, fileName):
#        self.file = fileName
#
#    def startFactory(self):
#        self.fp = open(self.file, 'a')
#
#    def stopFactory(self):
#        self.fp.close()


#for UDP only

class Logfile(DatagramProtocol):

    def startProtocol(self):
        m = datetime.datetime.now()
        dir=mkdir_p("%s/%s/%s/" % (m.year,m.month,m.day))
        self.filename = str(dir) + "log-%s.log" % int(time.time())
        self.fp = open(self.filename,'a',BLOCK_FILE_SIZE)

    def logWrite(self,data):
        self.fp.write(data+'\n')

        f_size = os.stat(self.filename).st_size
        if f_size > BLOCK_FILE_SIZE * 2:
            self.rollfile()
    #deferred processing to upllload?
    def rollfile(self):
        self.fp.close()
        oldfile = self.filename
        m = datetime.datetime.now()
        dir=mkdir_p("%s/%s/%s/" % (m.year,m.month,m.day))
        self.filename = str(dir) + "log-%s.log" % int(time.time())
        self.fp = open(self.filename,'a',BLOCK_FILE_SIZE)
        #boto is blocking, we do not want to block and spawn threads. that will suck
        #@todo: integrate with txaws (native twisted boto replacement for stream write)
        #import multipart
        #s3_path_key = "input/%s/" %  (adate)
       # sys.stdout.write("\n uploading to S3 path %s\n" % s3_path_key)
        #multipart.main(oldfile,'rzrlogs',s3_path_key+x,True,False)

    def _parse(self,data):
        lvl = fs_match.split(data)
        if lvl and len(lvl) > 1:
            i = int(lvl[1])
            fac = int(math.floor(i / 8))
            sev = i - (fac * 8)
            return (facility[fac], severity[sev])
        return (None, None)
    def datagramReceived(self, data,(host, port)):
#        print "%r" % self._parse(data)[0]
        self.logWrite(data)
#	print "%s" % data
reactor.listenUDP(PORT, Logfile())
reactor.run()
