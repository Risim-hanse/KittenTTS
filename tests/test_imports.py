def test_public_imports():
    import kittentts

    assert hasattr(kittentts, "KittenTTS")
