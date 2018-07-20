from prax import praxcmd


def test_main():
    assert praxcmd.main(["0x1234"]) == 0
    assert praxcmd.main(["-n", "p('asdf')"]) == 0
