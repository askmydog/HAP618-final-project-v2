from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from functions import age_parsing

class Notes(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    note: so.Mapped[str] = so.mapped_column(sa.String(1500))
    age: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    def __repr__(self):
        return f'{self.id}'