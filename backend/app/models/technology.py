from __future__ import annotations

import uuid

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Technology(Base):
    __tablename__ = "technologies"
    __table_args__ = (UniqueConstraint("name", name="uq_technologies_name"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    jobs = relationship(
        "Job",
        secondary="job_technologies",
        back_populates="technologies",
        lazy="selectin",
    )
