#coding=utf-8
__author__ = 'DM_'
from lib.TheradsPool import WorkerManager
from lib.ProxyList import ProxyList
from lib.IpMapsSaveLog import SaveLog
import lib.IpMapsArgv
import random,time,re
import requests

ProxyList = ProxyList
LogList = []
UnSolvedList = []
RetryList = {}
TargetIps = []
(options, args) = lib.IpMapsArgv.parser.parse_args()
Threads = options.Threads
MaxRetryTime = options.MaxRetryTime
TimeOut = options.TimeOut
TargetIp = options.Ip
RetryTime = 0

i = re.match(r"([\d]{1,3}.[\d]{1,3}.[\d]{1,3}.)",TargetIp)
for a in xrange(1,256):
    TargetIps.append(i.groups()[0]+str(a))

def IpToMap(ip):
    """

    :param ip: 传递进来的ip,返回其地理信息.
    """
    global UnSolvedList
    proxy = random.sample(ProxyList, 1)[0]
    proxies = dict(http=proxy)
    url = "http://www.maxmind.com/geoip/v2.0/city_isp_org/%s?demo=1" % ip

    try:
#        print(u"[+]当前IP:%s,当前代理:%s\r" % (ip,proxy))
#        print u"[+]当前IP:%s,当前代理:%s" % (ip, proxy)
        req = requests.get(url, proxies=proxies, timeout=TimeOut)
        HtmlContent = req.text
#        r = re.match("[\s\S]+?,(\"location\":[\s\S]+?})[\s\S]?",HtmlContent)
        r =re.match(r"[\s\S]+longitude\":([\d.]+)"
                    r"[\s\S]+latitude\":([\d.]+)"
                    r"[\s\S]+organization\":\"([\s\w]+)\",",HtmlContent)
        out = u"{Ip:'%s',Longitude:'%s',Latitude:'%s',organization:'%s'}"\
              % (ip,r.groups()[0],r.groups()[1],r.groups()[2])
        LogList.append(out)
        print u"[+]获取成功,当前IP:%s.\r" % ip
#        LogList.append(r.groups()[0])
    except:
        print(u"[-]获取失败.当前IP:%s,当前代理:%s.\r" % (ip, proxy))
#        print u"[-]失败,IP为:%s,代理为:%s,已添加至未完成日志表中." % (ip, proxy)
        UnSolvedList.append(ip)


def RetryUnSolvedList():
    global UnSolvedList

    print(u"[+]第%d次建立新的线程尝试未完成的工作.当前未完成数为%d,请稍候.\r" % (RetryTime,len(UnSolvedList)))

    CurrentUnSolveList = UnSolvedList[:]
    UnSolvedList = []
    UnSolvedListWm = WorkerManager(Threads)

    for ip in CurrentUnSolveList:
        RetryList[ip] = 0
        UnSolvedListWm.add_job(IpToMap,ip,)

    UnSolvedListWm.wait_for_complete()

    UnSolvedList=list(set(UnSolvedList))


def main():
    """

    """
    global UnSolvedList,RetryTime

    print "[+]Starting at:",time.ctime()
    print u"总数为:%d" % len(TargetIps)
    MainWorker = WorkerManager(Threads)
    for ip in TargetIps:
        MainWorker.add_job(IpToMap,ip,)

    MainWorker.wait_for_complete()

    UnSolvedList=list(set(UnSolvedList))
    while UnSolvedList and RetryTime < MaxRetryTime:
        RetryTime +=1
        RetryUnSolvedList()

    if UnSolvedList and RetryTime >=MaxRetryTime:
        print u"[-]超出最大重试次数.剩余ip请手工检测.总数为%d" % len(UnSolvedList)
        print UnSolvedList

    print "[+]All done at:",time.ctime()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print u"正在结束中."
        exit(0)
    logfile = open("log.txt",'a')
    logs = ''
    for log in LogList:
        logs += log + ','
    SaveLog(logs.encode('GBK'))
