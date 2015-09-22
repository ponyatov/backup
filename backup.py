
DIRS = [
        r'D:\w\backup',
        r'D:\parts',
        ]

NOREX1 = r'_[A-Z]+\\.+\.(GEM|PJ|dat\.xml|F[CS]T|bin|tpath)$'
NOREX2 = r'_[A-Z]+\\[A-Z]{2}[0-9]{5}$'
NOREX3 = r'\.(err)$' 
NOREX4 = r'\\\.git\\' 
NOREX5 = r'~$' 

FILES=[]

import os,sys,time,re,pickle
from stat import ST_MTIME

try:
    F=open('backup.db')
    DB=pickle.load(F)
    F.close()
except:
    DB={}

print time.localtime()[:6],sys.argv

NOW = '%.4i%.2i%.2i'%time.localtime()[:3]; print 'NOW',NOW

for D in DIRS:
    for X in os.walk(D):
        for F in X[-1]:
            FN=X[0]+'\\'+F
            if not ( 
                    re.findall(NOREX1,FN) or 
                    re.findall(NOREX2,FN) or
                    re.findall(NOREX3,FN) or
                    re.findall(NOREX4,FN) or
                    re.findall(NOREX5,FN)
                    ):
                MT=os.stat(FN)
                if FN not in DB:
                    FILES+=[FN]
                    DB[FN]=MT
                else:
                    if DB[FN]!=MT:
                        FILES+=[FN]
                        DB[FN]=MT

pickle.dump(DB,open('backup.db','w'))

FILES += ['%s.files'%NOW,'backup.db']
F=open('%s.files'%NOW,'w')
for i in FILES:
    print >>F,i ; print i
F.close()

CMD1 = 'winrar a -m5 -r D:\\backup\\%s @%s.files'%(NOW,NOW)
print time.localtime()[:6],CMD1,os.system(CMD1)
CMD2 = 'winrar a -m5 -r F:\\backup\\%s @%s.files'%(NOW,NOW)
print time.localtime()[:6],CMD2,os.system(CMD2)
CMD3 = 'winrar t F:\\backup\\%s '%NOW
print time.localtime()[:6],CMD3,os.system(CMD3)
raw_input('.')
