from cfg import *

import os,sys,time,datetime as dt,re,zlib
NOW='%.4i%.2i%.2i%.2i%.2i%.2i'%time.localtime()[:6]
print NOW,sys.argv ; print

import MySQLdb
db=MySQLdb.connect('localhost','root','gjyznjd','BACKUP',charset='utf8')

c0=db.cursor()
c0.execute("select count(0) from DAT")
DATsz=c0.fetchone()[0]
INTERVAL=dt.timedelta(days=PURGE_DAYS)/DATsz
BALSTART=dt.datetime.now()

c1=db.cursor()
c2=db.cursor()
c1.execute("select FN from DAT order by FN") ##
DONE=False
TS=BALSTART
while not DONE:
    T=c1.fetchone()
    if T:
        TS-=INTERVAL
        FN=re.sub(r'\\',r'\\\\',T[0])
        SQL="update DAT set TS='%s' where FN='%s'"%(TS.strftime("%Y-%m-%d %H:%M:%S"),FN)
        print SQL,
        print c2.execute(SQL)
    else:
        DONE=True
        
db.commit()
db.close()

raw_input('.')
