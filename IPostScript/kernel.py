from ipykernel.kernelbase import Kernel
from subprocess import check_output
import os.path
import re
import signal

from pexpect import replwrap, EOF
import pexpect

__version__ = "0.1.0"


class GSWrapper:
    """
    Wrap Ghostscript executable using pexpect
    """
    def __init__(self,
                 cmd = 'gs'
                 ):
        """
        todo: config cmd can be 'gs', 'gs-X11', etc.
        """
        self.p = pexpect.spawn(cmd)

        # maybe input/output to gs is always 'ascii'?
        self.encoding = "utf8"

        pattern1 = b"GS>"
        self.p.expect(re.compile(pattern1))

        assert(self.p.after == b"GS>")

        
    def run(self, code):
        """
        Execute 'code' in session.

        newline is appended
        """
        rx = re.compile(b'GS(>|<\d+>)')
        cc = code + "\n"

        # sendline uses "\r\n"?
        #p.sendline(c)
        self.p.send(cc)
        
        self.p.expect(rx)

        c1 = self.p.before.decode(self.encoding)

        code1 = code.strip()
        
        assert(c1.startswith(code1))
        r = c1[len(code1):]

        # .after is always the prompt itself. ?
        # eg:  b'GS>'
        #
        # could parse to get stack size
        # 'GS>', 'GS<1>', ...
        #

        return r.strip()
        

class PostscriptKernel(Kernel):
    """
    """
    implementation = 'postscript_kernel'
    implementation_version = __version__

    #printed on startup:
    banner = "PostScript kernel..."
    
    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.gs = GSWrapper()

    def do_execute(self,
                   code, silent, store_history=True,
                   user_expressions = None,
                   allow_stdin = False):

        result = self.gs.run(code)

        output = result

        if not silent:
            stream_content = {
                'name': 'stdout',
                'text': output,
            }
            self.send_response(
                self.iopub_socket,
                'stream',
                stream_content)

        return {
            'status': 'ok',
            # The base class increments the execution count
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
    
