from pytelemetry.remoting import translate

def test_translate_pass_thru():
    topic = "sometopic"
    top, opts = translate(topic)
    assert top == topic
    assert opts is None

def test_translate_simple_index():
    topic = "sometopic:0"
    top, opts = translate(topic)
    assert top == "sometopic"
    assert type(opts) == dict
    assert opts['index'] == 0

def test_translate_discard():
    topic = "12:sometopic"
    top, opts = translate(topic)
    assert top == "12:sometopic"
    assert opts is None
