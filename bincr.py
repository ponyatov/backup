EXCLUDES_REX=r'Thumbs\.db|.+\.swp|.+\~|.+\.py[cd]'

from cfg import *

import os,sys,time,datetime as dt,re,zlib
NOW='%.4i%.2i%.2i%.2i%.2i%.2i'%time.localtime()[:6]
print NOW,sys.argv ; print

ARCFILE=open('files','w')

import MySQLdb
db=MySQLdb.connect('localhost','root','gjyznjd','BACKUP',charset='utf8')

def FNQ(FN):
    return re.sub(r'\\',r'\\\\',SF)

c0=db.cursor()
c1=db.cursor()
c2=db.cursor()
c3=db.cursor()

# purge old DAT records forcing backup every N days
PURGE_TS=(dt.datetime.now()-dt.timedelta(days=PURGE_DAYS)).strftime('%Y-%m-%d %H:%M:%S')
c0.execute("delete from DAT where TS < '%s'"%PURGE_TS)

c1.execute("select PATH from dirs where OFF is null")
C1RES=c1.fetchall()
for DIR in map(lambda x:x[0],C1RES):
    for DR,t,FILES in os.walk(DIR):
        for FN in FILES:
            if not re.match(r'^(%s)$'%EXCLUDES_REX,FN):
                print ',',
                SF=DR+'\\'+FN
                #print 'SF',SF.encode('cp866')
                STAT=os.stat(SF)
                SZ=STAT.st_size #; print 'SZ',SZ
                MT=dt.datetime.fromtimestamp(STAT.st_mtime) ; MT=MT.replace(microsecond=0) #; print 'MT',MT
                if SZ<1024*1024*10: ## not't calc crc for large files
                    f=open(SF,'rb') ; CRC=zlib.adler32(f.read()) ; f.close()
                else:
                    CRC=0
                #print 'HASH',CRC
                c2.execute("select * from DAT where FN='%s'"%FNQ(SF))
                DEX=c2.fetchone() #; print 'DEX',DEX
                if not DEX:
                    SQL="insert into DAT values ('%s',NOW(),%i,%i,'%s')"%(FNQ(SF),SZ,CRC,MT)
                    #print SQL,c3.execute(SQL)
                    c3.execute(SQL)
                    print >>ARCFILE,SF.encode('cp866')
                else:
                    D_FN,D_TS,D_SZ,D_HASH,D_MT=DEX
                    if D_SZ <> SZ or D_HASH <> CRC or D_MT < MT :## or D_MT < MT : ## D_TS < MT or D_MT < MT or D_TS < D_MT or :
                        #print 'D_MT',D_MT
                        #print '  MT',  MT
                        print >>ARCFILE,SF.encode('cp866') 
                        SQL="update DAT set TS=NOW(),SZ=%i,HASH=%i,MT='%s' where FN='%s'"%(SZ,CRC,MT,FNQ(SF))
                        #print SQL,c3.execute(SQL)
                        c3.execute(SQL)
print
print

db.commit()
db.close()

MSQLDUMP="%s.mysql.dump"%NOW
os.system("mysqldump -u root --password=gjyznjd BACKUP > %s"%MSQLDUMP )
print >>ARCFILE,MSQLDUMP

ARCFILE.close()

os.system("rar a -m5 -o- -r C:\\backup\\%s.rar @files"%NOW)
os.system("copy /B /V C:\\backup\\%s.rar F:\\backup\\%s.rar"%(NOW,NOW))

raw_input('.')
os.remove(MSQLDUMP)
os.remove('files')



