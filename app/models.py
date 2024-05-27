import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime,timezone


class User(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    session_id: so.Mapped[int] = so.mapped_column(index=True,unique=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))
    equation: so.Mapped[str]=so.mapped_column(sa.String(64),index=True)
    lower_limit: so.Mapped[str]=so.mapped_column(sa.String(16),index=True)
    upper_limit: so.Mapped[str]=so.mapped_column(sa.String(16),index=True)
    steps: so.WriteOnlyMapped['StepList'] = so.relationship(
        back_populates='parent',passive_deletes=True)
    steps2: so.WriteOnlyMapped['StepList2'] = so.relationship(
        back_populates='parent',passive_deletes=True)
    megalist: so.WriteOnlyMapped['MegaList'] = so.relationship(
        back_populates='parent',passive_deletes=True)

    def __repr__(self):
        return f"({self.id}) {self.lower_limit} {self.upper_limit} {self.equation} {self.timestamp} {self.session_id}"
#redundant
class StepList(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    num_steps: so.Mapped[int] =so.mapped_column(index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))
    parent: so.Mapped[User] = so.relationship(back_populates='steps')

    def __repr__(self):
        return f"({self.id}) {self.num_steps} {self.timestamp} {self.parent}"

class StepList2(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    num_steps: so.Mapped[int] =so.mapped_column(index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))
    parent: so.Mapped[User] = so.relationship(back_populates='steps2')

    def __repr__(self):
        return f"({self.id}) {self.num_steps} {self.timestamp} {self.parent}"

class UserPreset(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    session_id: so.Mapped[int] = so.mapped_column(index=True,unique=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))
    equation: so.Mapped[str]=so.mapped_column(sa.String(64),index=True)

    def __repr__(self):
        return f"({self.id}) {self.equation} {self.timestamp} {self.session_id}"


class PixelString(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    session_id: so.Mapped[int] = so.mapped_column(index=True,unique=True)
    pix_str: so.Mapped[str]=so.mapped_column(sa.String(),index=True)

    def __repr__(self):
        return f"({self.id}) {self.pix_str} {self.session_id}"

class MegaList(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    x: so.Mapped[float] =so.mapped_column(index=True)
    y: so.Mapped[float] =so.mapped_column(index=True)
    mask_start: so.Mapped[int] = so.mapped_column(index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))
    parent: so.Mapped[User] = so.relationship(back_populates='megalist')

    def __repr__(self):
        return f"({self.id}) {self.x} {self.y} {self.mask_start} {self.timestamp} {self.parent}"
#redundant
class PixelString2(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    session_id: so.Mapped[int] = so.mapped_column(index=True,unique=True)
    tang_str: so.Mapped[str]=so.mapped_column(sa.String(),index=True)
    start_str: so.Mapped[str]=so.mapped_column(sa.String(),index=True)
    end_str: so.Mapped[str]=so.mapped_column(sa.String(),index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"({self.id}) {self.pix_str} {self.session_id}"

class PixelString3(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    session_id: so.Mapped[int] = so.mapped_column(index=True,unique=True)
    tang_str: so.Mapped[str]=so.mapped_column(sa.String(),index=True)
    start_str: so.Mapped[str]=so.mapped_column(sa.String(),index=True)
    end_str: so.Mapped[str]=so.mapped_column(sa.String(),index=True)
    ran_x: so.Mapped[float] =so.mapped_column(index=True)
    ran_num_steps: so.Mapped[int] =so.mapped_column(index=True)
    ran_tan_position: so.Mapped[int] =so.mapped_column(index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"({self.id}) {self.tang_str} {self.session_id} {self.timestamp}"