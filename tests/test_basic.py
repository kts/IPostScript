"""
Usage:
- pip install pytest
- `pytest tests`
  - from repo root

"""

def test_wrapper():
    """
    Run "1 2 add =" via GSWrapper and ensure we get '3'
    """
    from IPostScript.kernel import GSWrapper
    gs = GSWrapper()
    assert(gs.run("1 2 add =") == '3')

    
def test_platform():
    """
    test should work anywhere, so we just check
    that we can call is_windows() and get bool.
    """
    from IPostScript.kernel import is_windows
    assert(is_windows() in (True,False))

