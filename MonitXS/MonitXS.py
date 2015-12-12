#  MonitXS: A ZNC module to monitor and report xshellz suspicius activity
#  Copyright (C) 2015 noteness
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, download it from here: https://noteness.cf/GPL.txt
#  PDF: https://noteness.cf/GPL.pdf

import znc
import re
from fuzzywuzzy import fuzz
import os.path
import json
from collections import defaultdict

def defd():
    return {
    "nick": [],
    "hosts":[]
    }

class MonitXS(znc.Module):
    module_types = [znc.CModInfo.NetworkModule]
    description = "Tracks the keeps and approves in #xshellz"
    def OnLoad(self, args, message):
        self.path = self.GetSavePath()
        self.buffer = {}
        self.appr = re.compile(r'(\w+): (\w+), your account is approved and active!')
        self.kp = re.compile(r'(\w+): Shell with the name (\w+) have 336 hours active bonus (2 weeks) from now\.')
        self.db = os.path.join(self.path,'users.json')
        self.nd = defaultdict(defd)
        self.buf = os.path.join(self.path,'buffer.txt')
        self.reps = os.path.join(self.path,'reports.txt')
        if not os.path.exists(self.db):
            self.write()
        self.populate()
        return True

    def write(self):
        with open(self.db,'w') as f:
            json.dump(self.nd,f,indent=4)
        self.populate()

    def populate(self):
        with open(self.db,'r') as f:
            b = json.load(f)
        self.nd.update(b)

    def svreport(self, text):
        with open(self.reps,'a') as f:
            f.write(text+'\n')
            with open(self.buf,'a') as f:
                f.write(text+'\n')
        self.PutModule(text)

    def getreport(self):
        with open(self.reps,'r') as f:
            line = f.readline()
            while line:
                self.PutModule(line)
                line = f.readline()
        open(self.reps,'w').close()

    def OnChanMsg(self, nick, channel, message):
        if not channel.GetName() == "#xshellz":
            return znc.CONTINUE
        msg = str(message)
        msg = msg.split(" ")
        cmd = msg[0].lower()
        nickn = nick.GetNick()
        try:
            username = msg[1].lower()
        except IndexError:
            return znc.CONTINUE
        if cmd == '!keep' or cmd == '!approve':
            self.buffer[nickn] = dict(ni=nick,user=username)
        else:
            if not nickn == 'xinfo':
                return znc.CONTINUE
            res = self.appr.search(msg)
            if not res:
                res = self.kp.search(msg)
            if not res:
                return znc.CONTINUE
            nck = res.group(1)
            user = res.group(2)
            nd = self.buffer.get(nck,None)
            if nd:
                self.buffer.pop(nck,None)
                if user == nd['user']:
                    nu = nd['ni']
                    self.nd[user]['nick'].append(nck)
                    host = nu.GetHost()
                    if host == 'shell.xshellz.com':
                        host = None
                    self.nd['user']['hosts'].append(host)
                    for z,x in self.nd.items():
                        if z == user:
                            continue
                        if nck in x['nick']:
                            self.svreport("{0} is in the nick list for {1} ({2}) but user requested is {3} !att-nick-match".format(nck, z, " ,".join(x['nick']),user))
                            got = True
                        else:
                            for y in x['nick']:
                                if fuzz.ratio(y,host) >= 50:
                                    self.svreport("{0} is a fuzzy match against {1}'s nick {2}, but the user is {3} !att-nick-fuzzy-match".format(nck,z,y,user))
                        if host in x['hosts']:
                            got = True
                            self.svreport("{0}'s host ({4}) is in the host list for {1} ({2}) but user requested is {3} !att-host-match".format(nck, z, " ,".join(x['hosts']),user,host))
                        else:
                            for y in x['hosts']:
                                if fuxx.ratio(y,host) >= 95:
                                    self.svreport("{0} is a fuzzy match against {1}'s host {2}, but the user is {3} !att-host-fuzzy-match".format(host,z,y,user))
                        if fuzz.ratio(z,user) >= 50:
                            self.svreport("{0} is a fuzzy match against {1} !att-user-fuzzy-match".format(z,user))
                        if got:
                            break
                    self.write()
            return znc.CONTIUE

    def OnModCommand(self, cmd):
        self.PutModule("This module doesn't take any commands")

    def OnClientLogin(self):
        self.getreport()
                                    



