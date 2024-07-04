import sqlalchemy as sa
from sqlalchemy.orm import Mapped,mapped_column,relationship,WriteOnlyMapped
from app import db
from datetime import datetime,timezone


class User(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True)
    cookie_code: Mapped[str] = mapped_column(sa.String(12),unique=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    equation: Mapped[str]=mapped_column(sa.String(64))
    lower_limit: Mapped[str]=mapped_column(sa.String(16))
    upper_limit: Mapped[str]=mapped_column(sa.String(16))

    def __repr__(self):
        return f"({self.id}) {self.lower_limit} {self.upper_limit} {self.equation} {self.timestamp} {self.cookie_code}"


class StepList2(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True)
    num_steps: Mapped[int] =mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    cookie_code: Mapped[str] = mapped_column(sa.String(12))

    def __repr__(self):
        return f"({self.id}) {self.num_steps} {self.timestamp} {self.cookie_code}"

class UserPreset(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True)
    cookie_code: Mapped[str] = mapped_column(index=True,unique=True)
    timestamp: Mapped[datetime] = mapped_column(index=True,default=lambda: datetime.now(timezone.utc))
    equation: Mapped[str]= mapped_column(sa.String(64),index=True)

    def __repr__(self):
        return f"({self.id}) {self.equation} {self.timestamp} {self.cookie_code}"


class PixelString(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True)
    cookie_code: Mapped[str] = mapped_column(unique=True)
    pix_str: Mapped[str]=mapped_column(sa.String()) #pix_str name should be img_url
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"({self.id}) {self.pix_str} {self.cookie_code} {self.timestamp}"

class MegaList(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True)
    x: Mapped[float] =mapped_column()
    y: Mapped[float] =mapped_column()
    mask_start: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    cookie_code: Mapped[str] = mapped_column(sa.String(12))

    def __repr__(self):
        return f"({self.id}) {self.x} {self.y} {self.mask_start} {self.timestamp} {self.cookie_code}"


class PixelString3(db.Model):
    id: Mapped[int]=mapped_column(primary_key=True)
    cookie_code: Mapped[str] = mapped_column(index=True,unique=True)
    tang_str: Mapped[str]=mapped_column(sa.String())#for str
    start_str: Mapped[str]=mapped_column(sa.String())#replace
    end_str: Mapped[str]=mapped_column(sa.String())#with url
    ran_x: Mapped[float] =mapped_column(index=True)
    ran_num_steps: Mapped[int] =mapped_column(index=True)
    ran_tan_position: Mapped[int] =mapped_column(index=True)
    timestamp: Mapped[datetime] = mapped_column(index=True,default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"({self.id}) {self.tang_str} {self.cookie_code} {self.timestamp}"