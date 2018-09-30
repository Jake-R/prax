from prax import praxcmd
from contextlib import redirect_stdout
import io

def get_stdout(capsys, func, args):
    retval = func(args)
    cap = capsys.readouterr()
    return retval, cap.out

def test_cmd(capsys):
    assert get_stdout(capsys, praxcmd.main, ["0x1234"]) == (0, '\x12\x34\n')

def test_no_newline(capsys):
    assert get_stdout(capsys, praxcmd.main, ["-n", "p('asdf')"]) == (0, 'asdf')

def test_multiline_cnmd(capsys):
    assert get_stdout(capsys, praxcmd.main, ['x="asdf";x*8']) == (0, "asdf"*8 + "\n")

def test_hexdump(capsys):
    assert get_stdout(capsys, praxcmd.main, ['p(0x1234) + "asdf"*4', '--hd']) == (0,
"""00000000  12 34 61 73  64 66 61 73  64 66 61 73  64 66 61 73  │·4as│dfas│dfas│dfas│
00000010  64 66                                               │df│
00000012

""")


