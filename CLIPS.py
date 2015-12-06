import os
from subprocess import Popen, PIPE

class CLIPSError(Exception): pass
class InvalidMessage(Exception): pass

class CLIPS(object):
    def __init__(self, *cmds, exe=None, prompt="CLIPS> ", maxread=1024):
        if not exe:
            if os.name == 'nt':
                exe = r"C:\Program Files (x86)\CLIPS\CLIPSDOS64.exe"
            else:
                exe = "clips"
        # setup vars
        self.exe = exe
        self.prompt = prompt
        self.maxread = maxread
        self.output = ""
        # start up clips
        self.startCLIPS()
        # loop through cmd
        for cmd in cmds:
            self.sendRecv(cmd)

    def startCLIPS(self):
        self.pipe = Popen([self.exe], stdin=PIPE, stdout=PIPE, bufsize=0)
        self.recv()

    def sendRecv(self, cmd):
        self.send(cmd)
        return self.recv()

    def send(self, cmd):
        if not validmessage(cmd):
            raise InvalidMessage
        writeBytes = (cmd + '\n').encode()
        self.pipe.stdin.write(writeBytes)

    def recv(self):
        # read until prompt
        self.output = ""
        # this loop is terrible
        while self.output.find(self.prompt) == -1:
            self.output += self.pipe.stdout.read(self.maxread).decode()
        pos = self.output.find(self.prompt)
        result = self.output[:pos]
        self.output = self.output[pos+len(self.prompt):]
        return result

    def defrule(self, name, lhs, rhs):
        o = self.sendRecv("(defrule " + name + lhs + " => " + rhs + ")")
        if o:
            raise CLIPSError

    def deffacts(self, name, *facts):
        print("(deffacts " + name + " ".join(facts) + ")")
        o = self.sendRecv("(deffacts " + name + " ".join(facts) + ")")
        if o:
            raise CLIPSError

    def assertFact(self, *facts):
        return self.sendRecv("(assert " + " ".join(facts) + ")")

    def clear(self):
        self.sendRecv("(clear)")

    def reset(self):
        self.sendRecv("(reset)")

    def run(self, num=""):
        return self.sendRecv("(run %s)" %(num))

    def facts(self):
        lines = self.sendRecv("(facts)").split("\n")[:-2]
        result = {}
        for line in lines:
            indexStr, fact = line.split()
            index = int(indexStr[2:])
            result[index] = fact
        return result

    def printFacts(self):
        print(self.sendRecv("(facts)"), end='')

    def agenda(self):
        # TODO make it good
        print(self.sendRecv("(agenda)"), end='')

    def exit(self):
        self.send('(exit)')

    def load(self, name):
        self.sendRecv('(load "' + name + '")')

    def exit(self):
        self.send("(exit)")

def validmessage(s):
    st = []
    quote = False
    idx = len(s)
    for i, c in enumerate(s):
        if c == '(':
            if not quote:
                st.insert(0, c)
        elif c == ')':
            if not quote:
                if not st:
                    return False
                elif st[0] == '(':
                    st.pop()
                else:
                    return False
        elif c == '"':
            quote = not quote
        elif c == ';' and not quote:
            idx = i
            break
    s = s[:idx] # strip comment
    return not(bool(st)) and not quote and bool(s.strip())
