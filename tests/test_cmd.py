# -*- coding: utf-8 -*-

from prax import praxcmd, p
from hypothesis import given, example, strategies as st


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
    res = get_stdout(capsys, praxcmd.main, ['p(0x1234) + "asdf"*4', '--hd'])
    assert res[0] == 0

@given(st.integers().filter(lambda x: x>0))
def test_cmdraw(capfdbinary, int_):
    retval, stdout = get_stdout(capfdbinary, praxcmd.main, [str(int_), '-n'])
    assert (retval, p(stdout)) == (0, p(int_).bytes)

def test_syntax_error():
    assert praxcmd.main(["p("]) != 0
