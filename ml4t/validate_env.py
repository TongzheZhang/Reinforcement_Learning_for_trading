"""MLT: Validate development environment."""

import sys

def check_python_version(target_major=2, target_minor=7, target_micro_min=5):
    """Check Python version."""
    version_check_str = "Python {}.{}.{} (desired: {}.{}.{}+)".format(
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro,
            target_major, target_minor, target_micro_min)
    assert (sys.version_info.major == target_major and
            sys.version_info.minor == target_minor and
            sys.version_info.micro >= target_micro_min), \
            version_check_str
    print version_check_str


def test_pandas():
    """Test pandas functionality."""
    df = pandas.DataFrame(numpy.random.randn(5, 4))
    print "pandas.DataFrame with random values:\n", df


def test_data():
    """Test for historical stock data."""
    symbols = ['SPY', 'GOOG', 'AAPL', 'GLD', 'XOM']
    for symbol in symbols:
        data = pandas.read_csv("data/{}.csv".format(symbol))
        print "{}:".format(symbol)
        print data.head(2)


def validate_env():
    """Validate development environment."""
    # List of required libraries and desired versions
    libs = [('numpy', '1.6.1+'), ('matplotlib', '1.1.0+'), ('pandas', '0.7.3+'), ('scipy', '0.9.0+'), ('dateutil', '1.5+'), ('setuptools', '0.6+'), ('datetime', None)]
    try:
        # Check Python version
        check_python_version()

        # Check for required libraries
        import importlib
        for lib_name, lib_ver in libs:
            lib_imported = importlib.import_module(lib_name)
            print "{} {} (desired: {})".format(lib_name,
                    lib_imported.__version__ if '__version__' in dir(lib_imported) else 'n/a',
                    lib_ver if lib_ver is not None else 'n/a')
            globals()[lib_name] = lib_imported

        # Test pandas functionality
        test_pandas()

        # Test for historical stock data
        test_data()

        print "Passed!"
    except (AssertionError, ImportError) as e:
        print >> sys.stderr, "Failed:", e


if __name__ == "__main__":
    validate_env()
