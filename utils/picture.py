import sys
import os
import urllib
try :
    from urllib.request import urlopen
except ImportError :
    from urllib import urlopen
from roundup import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

valid = db.user_status.lookup ('valid')
http  = "http://www.vie.at.tttech.ttt/company/staff/pics/%s.jpg"

def addpic (user, pic) :
    f = db.file.create \
        (name = str (user.nickname), type = 'image/jpeg', content = pic)
    np = user.pictures
    np.append (f)
    db.user.set (user.id, pictures = np)
# end def addpic

for u in db.user.list () :
    user = db.user.getnode (u)
    if user.status != valid :
        continue
    if not user.nickname :
        print "     no nickname:", user.username
        continue
    try :
        pic = urlopen(http % user.nickname.lower()).read()
    except IOError :
        print "          no pic:", user.username
        continue
    if pic [6:10] != 'JFIF' :
        print "     invalid pic:", user.username
        continue
    for n, p in enumerate (reversed (user.pictures)) :
        rpic = db.file.get (p, 'content')
        # special case where pic was removed in db
        if len (rpic) == 0 :
            #db.file.set (p, content = pic)
            break
        if rpic == pic :
            if not n :
                print "    matching pic:", user.username
                break
            else :
                print "Ooops: old picture matches:", user.username, n
                break
        else :
            print "non-matching pic:", user.username
    else :
        print "      create pic:", user.username
        addpic (user, pic)
db.commit ()
