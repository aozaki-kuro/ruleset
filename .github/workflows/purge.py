import commands
import json
import os
import time
import urllib2

def purge(branch):
    url="https://purge.jsdelivr.net/gh/ACL4SSR/ACL4SSR@%s/" % branch
    response=json.loads(urllib2.urlopen(urllib2.Request(url)).read(),strict=False)
    print response
    time.sleep(180)
    return check(branch)

def check(branch):
    gitmd5=os.environ['GITMD5']
    print gitmd5
    os.system('python jsdelivr_dl.py https://github.com/aozaki-kuro/ruleset ' + branch + ' ' + branch)
    os.system('cd ' + branch)
    branchmd5 = commands.getoutput('cat *.acl |md5sum')
    print branchmd5
    os.system('cd ' + branch + '&& rm -rf '+ branch)
    return (gitmd5==branchmd5)
    
def run(branch):
    count=0
    result=check(branch)
    if result==True:
        print ('Already Up-to-Date!')
    while(count<=4 and result==False):
        result=purge(branch)
        count=count+1
        if result==True:
            print ("Purge Branch %s Success!" % branch)
    return result
    
def main():
    latest=run("latest")
    master=run("master")
    
    if (master and latest)==True:
        exit(0)
    else:
        exit(1)
    
if __name__ == '__main__':
    main()
