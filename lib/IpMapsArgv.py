#coding=utf-8
__author__ = 'DM_'
from optparse import OptionParser

parser = OptionParser(usage="usage:%prog [optinos]")
parser.add_option("--timeout",
                  action="store",
                  type='int',
                  dest="TimeOut",
                  help=u"连接超时设定,默认为5秒.",
                  default=5
)
parser.add_option("-i", "--ip",
                  action="store",
                  dest="Ip",
                  type="string",
                  help=u"目标站点ip."
)
parser.add_option("-t", "--threads",
                  action="store",
                  dest="Threads",
                  type="int",
                  help=u"最大运行的线程数,默认为10,最大不要超过30.",
                  default=10
)
parser.add_option("-m","--MaxRetryTime",
                  action="store",
                  dest="MaxRetryTime",
                  type="int",
                  help=u"最大尝试次数.默认为5.",
                  default=5
)
