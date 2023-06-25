from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    GENDER = (
        ("MALE", "male"),
        ("FEMALE", "female"),
    )

    ROLES = (
        ("ADMIN", "admin"),
        ("USER", "user")
    )
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    gender = Column(ChoiceType(choices=GENDER), default="MALE")
    roles = Column(ChoiceType(choices=ROLES), default="USER")

    def __repr__(self):
        return f"<User {self.username}"
