from flask_migrate import MigrateCommand
from flask_script import Manager

from hr_helper import app
from hr_helper.utils.utilities import SuperUser


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('super_user', SuperUser)


if __name__ == "__main__":
    manager.run()
