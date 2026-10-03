def test_two_plus_two(record_property):
    record_property("proves", "31.1")
    assert 2 + 2 == 4


def test_greeting(record_property):
    record_property("proves", "31.2")
    greeting = "helo"
    assert greeting == "hello"
