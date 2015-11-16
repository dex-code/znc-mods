#xKeep

This module keeps your account at #xshellz

##Requirements

* [ZNC][1]
* [Modpython][2] module in ZNC

##Commands

`set username <user>`: Sets your xshellz username to `<user>` (You should do this the first time)
`set rcpt <name>`: Whom to send the keep msg to (Either xinfo or #xshellz also You should do this the first time)
`fexec`: Sends your keep for the first time (You should set recipient and username before using this command)
`help`: Shows help

##Usage

Download this script and put this in your ZNC modules dir and load it (`/quote znc loadmod xKeep`)

Then set your xshellz username by typing `/msg *xKeep set username <your user>` in your client
Then set your recipient by typing `/msg *xKeep set rcpt <xinfo or #xshellz` after these type `/msg *xKeep fexec` Viola! it's set and now, you would never need to have to worry about your account timing out! :D

[1]: http://wiki.znc.in/
[2]: http://wiki.znc.in/Modpython/