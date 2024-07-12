from app.database import db
from sqlalchemy.orm import Mapped, mapped_column


class Product(db.Model):
    id: Mapped[int] = db.mapped_column(primary_key=True)
    name: Mapped[str] = db.mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Product {self.id}|{self.name}>"
