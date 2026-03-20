

def pytest_addoption(parser):
    parser.addoption(
        "--default-path",
        action="store",
        default="tests/",
        help="default path for pytest",
    )


def pytest_configure(config):
    config.option.file_or_dir = config.getoption("--default-path")
