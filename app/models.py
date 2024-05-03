import sqlalchemy as sa
import sqlalchemy.orm as so
#from app import db

"""
class UserInput(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    equation: so.Mapped[str]=so.mapped_column(sa.String(64),index=True)
    lower_limit: so.Mapped[str]=so.mapped_column(sa.String(16),index=True)
    upper_limit: so.Mapped[str]=so.mapped_column(sa.String(16),index=True)

    def __repr__(self):
        return '<Equation {}>'.format(self.equation)

"""