def pytest_configure(config):
    config.addinivalue_line("markers", "firebase: mark test as requiring Firebase (skip by default)")
