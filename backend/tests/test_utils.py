from mixmatch.core.utils import replace_list_item


def test_replace_list_item():
    assert replace_list_item([], 0, 'test0') == ['test0']
    assert replace_list_item(['test0'], 0, 'test0') == ['test0']
    assert replace_list_item(['test'], 0, 'test0') == ['test0']
    assert replace_list_item(['test', 'test1'], 0, 'test0') == ['test0', 'test1']
    assert replace_list_item(['test', 'test1', 'test2'], 0, 'test0') == ['test0', 'test1', 'test2']
    assert replace_list_item(['test0', 'test', 'test2'], 1, 'test1') == ['test0', 'test1', 'test2']
    assert replace_list_item(['test0', 'test1', 'test'], 2, 'test2') == ['test0', 'test1', 'test2']
