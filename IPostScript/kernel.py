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

    langauge_info = {
        'name': 'PostScript',
        'mimetype': 'text/postscript',

        #others:
        #codemirror_mode
        #pygments_lexer
    }
    
    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.gs = GSWrapper()

        ##
        ## keywords for tab-completion
        ##
        self.keywords = [
'$error',
 '<<',
 '=',
 '==',
 '>>',
 'FontDirectory',
 'GlobalFontDirectory',
 'ISOLatin1Encoding',
 'StandardEncoding',
 'UserObjects',
 'VMerror',
 '[',
 ']',
 'abs',
 'add',
 'aload',
 'anchorsearch',
 'and',
 'arc',
 'arcn',
 'arct',
 'arcto',
 'array',
 'ashow',
 'astore',
 'atan',
 'awidthshow',
 'begin',
 'bind',
 'bitshift',
 'bytesavailable',
 'cachestatus',
 'ceiling',
 'charpath',
 'clear',
 'cleardictstack',
 'cleartomark',
 'clip',
 'clippath',
 'cliprestore',
 'clipsave',
 'closefile',
 'closepath',
 'colorimage',
 'composefont',
 'concat',
 'concatmatrix',
 'configurationerror',
 'copy',
 'copypage',
 'cos',
 'count',
 'countdictstack',
 'countexecstack',
 'counttomark',
 'cshow',
 'currentblackgeneration',
 'currentcacheparams',
 'currentcmykcolor',
 'currentcolor',
 'currentcolorrendering',
 'currentcolorscreen',
 'currentcolorspace',
 'currentcolortransfer',
 'currentdash',
 'currentdevparams',
 'currentdict',
 'currentfile',
 'currentflat',
 'currentfont',
 'currentglobal',
 'currentgray',
 'currentgstate',
 'currenthalftone',
 'currenthsbcolor',
 'currentlinecap',
 'currentlinejoin',
 'currentlinewidth',
 'currentmatrix',
 'currentmiterlimit',
 'currentobjectformat',
 'currentoverprint',
 'currentpacking',
 'currentpagedevice',
 'currentpoint',
 'currentrgbcolor',
 'currentscreen',
 'currentsmoothness',
 'currentstrokeadjust',
 'currentsystemparams',
 'currenttransfer',
 'currentundercolorremoval',
 'currentuserparams',
 'curveto',
 'cvi',
 'cvlit',
 'cvn',
 'cvr',
 'cvrs',
 'cvs',
 'cvx',
 'def',
 'defaultmatrix',
 'definefont',
 'defineresource',
 'defineuserobject',
 'deletefile',
 'dict',
 'dictfull',
 'dictstack',
 'dictstackoverflow',
 'dictstackunderflow',
 'div',
 'dtransform',
 'dup',
 'echo',
 'end',
 'eoclip',
 'eofill',
 'eq',
 'erasepage',
 'errordict',
 'exch',
 'exec',
 'execform',
 'execstack',
 'execstackoverflow',
 'execuserobject',
 'executeonly',
 'executive',
 'exit',
 'exp',
 'false',
 'file',
 'filenameforall',
 'fileposition',
 'fill',
 'filter',
 'findcolorrendering',
 'findencoding',
 'findfont',
 'findresource',
 'flattenpath',
 'floor',
 'flush',
 'flushfile',
 'for',
 'forall',
 'gcheck',
 'ge',
 'get',
 'getinterval',
 'globaldict',
 'glyphshow',
 'grestore',
 'grestoreall',
 'gsave',
 'gstate',
 'gt',
 'handleerror',
 'identmatrix',
 'idiv',
 'idtransform',
 'if',
 'ifelse',
 'image',
 'imagemask',
 'index',
 'ineofill',
 'infill',
 'initclip',
 'initgraphics',
 'initmatrix',
 'instroke',
 'interrupt',
 'inueofill',
 'inufill',
 'inustroke',
 'invalidaccess',
 'invalidexit',
 'invalidfileaccess',
 'invalidfont',
 'invalidrestore',
 'invertmatrix',
 'ioerror',
 'itransform',
 'known',
 'kshow',
 'languagelevel',
 'le',
 'length',
 'limitcheck',
 'lineto',
 'ln',
 'load',
 'log',
 'loop',
 'lt',
 'makefont',
 'makepattern',
 'mark',
 'matrix',
 'maxlength',
 'mod',
 'moveto',
 'mul',
 'ne',
 'neg',
 'newpath',
 'noaccess',
 'nocurrentpoint',
 'not',
 'null',
 'nulldevice',
 'or',
 'packedarray',
 'pathbbox',
 'pathforall',
 'pop',
 'print',
 'printobject',
 'product',
 'prompt',
 'pstack',
 'put',
 'putinterval',
 'quit',
 'rand',
 'rangecheck',
 'rcheck',
 'rcurveto',
 'read',
 'readhexstring',
 'readline',
 'readonly',
 'readstring',
 'realtime',
 'rectclip',
 'rectfill',
 'rectstroke',
 'renamefile',
 'repeat',
 'resetfile',
 'resourceforall',
 'resourcestatus',
 'restore',
 'reversepath',
 'revision',
 'rlineto',
 'rmoveto',
 'roll',
 'rootfont',
 'rotate',
 'round',
 'rrand',
 'run',
 'save',
 'scale',
 'scalefont',
 'search',
 'selectfont',
 'serialnumber',
 'setbbox',
 'setblackgeneration',
 'setcachedevice',
 'setcachedevice2',
 'setcachelimit',
 'setcacheparams',
 'setcharwidth',
 'setcmykcolor',
 'setcolor',
 'setcolorrendering',
 'setcolorscreen',
 'setcolorspace',
 'setcolortransfer',
 'setdash',
 'setdevparams',
 'setfileposition',
 'setflat',
 'setfont',
 'setglobal',
 'setgray',
 'setgstate',
 'sethalftone',
 'sethsbcolor',
 'setlinecap',
 'setlinejoin',
 'setlinewidth',
 'setmatrix',
 'setmiterlimit',
 'setobjectformat',
 'setoverprint',
 'setpacking',
 'setpagedevice',
 'setpattern',
 'setrgbcolor',
 'setscreen',
 'setsmoothness',
 'setstrokeadjust',
 'setsystemparams',
 'settransfer',
 'setucacheparams',
 'setundercolorremoval',
 'setuserparams',
 'setvmthreshold',
 'shfill',
 'show',
 'showpage',
 'sin',
 'sqrt',
 'srand',
 'stack',
 'stackoverflow',
 'stackunderflow',
 'start',
 'startjob',
 'status',
 'statusdict',
 'stop',
 'stopped',
 'store',
 'string',
 'stringwidth',
 'stroke',
 'strokepath',
 'sub',
 'syntaxerror',
 'systemdict',
 'timeout',
 'token',
 'transform',
 'translate',
 'true',
 'truncate',
 'type',
 'typecheck',
 'uappend',
 'ucache',
 'ucachestatus',
 'ueofill',
 'ufill',
 'undef',
 'undefined',
 'undefinedfilename',
 'undefinedresource',
 'undefinedresult',
 'undefinefont',
 'undefineresource',
 'undefineuserobject',
 'unmatchedmark',
 'unregistered',
 'upath',
 'userdict',
 'usertime',
 'ustroke',
 'ustrokepath',
 'version',
 'vmreclaim',
 'vmstatus',
 'wcheck',
 'where',
 'widthshow',
 'write',
 'writehexstring',
 'writeobject',
 'writestring',
 'xcheck',
 'xor',
 'xshow',
 'xyshow',
 'yshow']


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
    
    def do_complete(self, code, cursor_pos):
        """
        keyword completion

        see,
        https://jupyter-client.readthedocs.io/en/latest/wrapperkernels.html#MyCustomKernel.do_complete
        """
        out = {
            'status':       'ok',
            
            'matches':      [],

            # range of text that should be replaced:
            'cursor_start': 0,
            'cursor_end':   cursor_pos, #typically == cursor_pos

            'metadata':     dict(),
        }

        ##
        ## Matching a bit limited right now:
        ## - we loop through all keywords. to be
        ##   more efficient, we could try to
        ##   pre-built a trie-like data structure
        ##   to immediately check prefixes.
        ## 
        ## - we use .split() to do a basic
        ##   tokenization (since completion is
        ##   done on the last/current token).
        ##   This might not always be right..
        ##
        
        c = code[:cursor_pos]
        if len(c) > 0:
            sp = c.split()
            if len(sp) > 0:
                to_match = sp[-1]

                matches = []
                
                for keyword in self.keywords:
                    if keyword.startswith(to_match):
                        matches.append(keyword)

                if len(matches) > 0:
                    out['matches']      = matches
                    out['cursor_start'] = cursor_pos - len(to_match)
                    out['cursor_end']   = cursor_pos

        return out
