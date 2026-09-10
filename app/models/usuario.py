from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    role = Column(String, nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)