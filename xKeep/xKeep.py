# Copyright (c) 2015 noteness
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE

import znc
from datetime import timedelta
import time

class txkeep(znc.Timer):
    def RunJob(self):
        mod = self.GetModule()
        rcpt = mod.recpt
        username = mod.user
        mod.PutIRC('PRIVMSG {0} :!keep {1}'.format(recv, username))
        mod.lastkeep = time.time()

class xKeep(znc.Module):
    module_types = [znc.CModInfo.NetworkModule]
    description = "Keeps your account at xShellz"
    week = 604800
    def OnLoad(self, args, message):
        try:
            self.lastkeep = float(self.nv['lastkeep'])
        except KeyError:
            self.lastkeep = None
        try:
            self.rcpt = self.nv['rcpt']
        except KeyError:
            self.rcpt = None
        try:
            self.user = self.nv['user']
        except KeyError:
            self.user = None
        try:
            self.firstload = bool(self.nv['firstload'])
        except KeyError:
            self.firstload = True
        if not self.firstload:
            diff = timedelta(seconds= time.time()) - timedelta(seconds=lastkeep)
            diff = (diff.days * 24 * 60 *60) + (diff.seconds)
            if diff >= week:
                self.sleep(0)
            else:
                self.PutModule("Time remaining for the next keep: {0}".format(diff))
                dif = week - diff
                self.sleep(dif)
        return True
    def keep(self):
        rcpt = self.rcpt
        username = self.user
        self.PutIRC('PRIVMSG {0} :!keep {1}'.format(recv, username))
        self.lastkeep = time.time()
        self.PutModule('Keep command sent')
        self.nv['lastkeep'] = str(self.lastkeep)

    def fexec(self):
        if (self.user and seld.rcpt):
            self.sleep(0)
            self.firstload = False
            self.nv['firstload'] = 'False'
            self.PutModule('Keep command sent')
        else:
            self.PutModule("Are you sure that you have set username and recipient?")

    def sleep(self, time):
        time.sleep(time)
        self.keep()
        self.timer = txkeep(interval = self.week, cycle = 0)

    def setrcpt(self, rcpt):
        self.rcpt = rcpt
        self.nv['rcpt'] = rcpt
        self.PutModule("Recipient Set to {0}".format(self.rcpt))

    def onhelp(self):
        self.PutModule("+--------------+---------------------+-------------------------------------------------------------------+")
        self.PutModule("| Command      | Arguments           | Help                                                              |")
        self.PutModule("+--------------+---------------------+-------------------------------------------------------------------+")
        self.PutModule("| set username | set username <user> | Set your xshellz username (You should do this first)              |")
        self.PutModule("+--------------+---------------------+-------------------------------------------------------------------+")
        self.PutModule("| set rcpt     | set rcpt <text>     | Where to send the message (xinfo or #xshellz)                     |")
        self.PutModule("+--------------+---------------------+-------------------------------------------------------------------+")
        self.PutModule("| fexec        | fexec               | Starts the module for the first time                              |")
        self.PutModule("|              |                     | (You should set username and recipient before using this command) |")
        self.PutModule("+--------------+---------------------+-------------------------------------------------------------------+")
        self.PutModule("| help         | help                | Shows this help                                                   |")
        self.PutModule("+--------------+---------------------+-------------------------------------------------------------------+")

    def setuser(self, user):
        self.user = user
        self.nv['user'] = user
        self.PutModule("Username set t {0}".format(self.user))

    def OnModCommand(self, command):
        cmdsplit = command.split()
        cmds = ['set','fexec','help']
        cmd = cmdsplit[0]
        try:
            subcmd = cmdsplit[1]
        except IndexError:
            subcmd = None
        try:
            args = cmdsplit[2]
        except IndexError:
            args = None
        if len(cmdsplit) > 3:
            self.PutModule("There are more arguments than required")
            return

        if cmd == 'help':
            self.onhelp()
        elif cmd == 'set':
            if not args:
                self.PutModule("No arguments given")
                return
            if subcmd == 'username':
                self.setuser(args)
                return
            elif subcmd == 'rcpt':
                self.setrcpt(args)
            else:
                self.PutModule("Invalid Command")
                return
        elif cmd == 'fexec':
            self.fexec()
        else:
            self.PutModule("Invalid Command")

