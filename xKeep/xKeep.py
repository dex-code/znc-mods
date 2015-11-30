#  Xkeep: A ZNC module that keeps your account at #xshellz
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
from datetime import timedelta
import time

class txKeep(znc.Timer):
    def RunJob(self):
        mod = self.GetModule()
        mod.keep()

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
        msg = 'PRIVMSG {0} :!keep {1}'.format(rcpt, username)
        self.PutIRC(msg)
        self.lastkeep = time.time()
        self.PutModule('Keep command sent')
        self.nv['lastkeep'] = str(self.lastkeep)

    def fexec(self):
        if (self.user and self.rcpt):
            self.sleep(0)
            self.firstload = False
            self.nv['firstload'] = 'False'
            self.PutModule('Keep command sent')
        else:
            self.PutModule("Are you sure that you have set username and recipient?")

    def sleep(self, tme):
        time.sleep(tme)
        self.keep()
        self.timr = self.CreateTimer(txKeep ,interval = self.week, cycles = 0)

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
        self.PutModule("Username set to {0}".format(self.user))

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

