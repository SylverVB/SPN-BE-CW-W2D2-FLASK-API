from app.database import db
from sqlalchemy.orm import Mapped, mapped_column


class Customer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(255), nullable=False) # nullable=False - not allow the first_name to be nullable (zero or null)
    last_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    username: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Customer {self.id}|{self.username}>"