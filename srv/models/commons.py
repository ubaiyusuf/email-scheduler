"""
This file contains commons models
"""
from datetime import datetime

import flask_sqlalchemy as fsa
import sqlalchemy as sa

from srv import db


class BaseModel(db.Model):  # pragma: no cover
    """
    This class is the abstract model that inherited for other model
    """

    __abstract__ = True

    created_at = sa.Column(
        sa.DateTime(),
        default=sa.func.now(),
        server_default=sa.func.now(),
        nullable=False,
    )
    updated_at = sa.Column(
        sa.DateTime(),
        default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
    is_deleted = sa.Column(sa.Boolean(), default=False, server_default="false")

    def save(self) -> "BaseModel":
        """
        This method used to add new record to table or update existing record

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception:
            db.session.rollback()
            raise

    def add_flush(self) -> "BaseModel":
        """
        This method similar with save, but use flush method of sqlalchemy instead of commit

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception:
            db.session.rollback()
            raise

    def delete(self) -> "BaseModel":
        """
        This method used to mark the record to deleted

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            self.is_deleted = True
            self.deleted_at = datetime.now()

            db.session.add(self)
            db.session.commit()
            return self

        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def base_query(cls) -> fsa.BaseQuery:
        """
        This method used to get base query that remove soft deleted file

        Returns:
            fsa.BaseQuery -- [Base query object]
        """
        return cls.query.filter_by(is_deleted=False)
