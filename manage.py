from ivr_phone_tree_python import app
from flask.ext.script import Server, Manager
import os

#port = 5000
#if 'PORT' in os.environ.keys():
#    port = os.environ['PORT']
port = int(os.getenv("PORT"))

manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', port=port))


@manager.command
def test():
    """Run the unit tests."""
    import sys, unittest
    tests = unittest.TestLoader().discover('.', pattern="*_tests.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not result.wasSuccessful():
            sys.exit(1)


if __name__ == "__main__":
    manager.run()
