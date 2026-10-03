def test_addition(record_property):
    record_property("proves", "10.1")
    assert 2 + 2 == 4


def test_greeting(record_property):
    record_property("proves", "10.2")
    greeting = "helo"
    assert greeting == "hello"
