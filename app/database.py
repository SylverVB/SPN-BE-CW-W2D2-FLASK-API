from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

# migrate = Migrate(command='abc') if we want a different command other than db (currently: flask db)
# migrate = Migrate(directory='database migrations by Victor') if we want a different directory other than migrations (currently: migrations)

