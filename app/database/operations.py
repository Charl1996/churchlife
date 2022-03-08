from sqlalchemy.orm import Session
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from app.database.exceptions import *


class DBOperations:

    @classmethod
    def commit_to_db(cls, db: Session, model: any):
        try:
            db.add(model)
            db.commit()
            db.refresh(model)
            return model
        except IntegrityError:
            db.rollback()
            raise DuplicateResourceError
        except PendingRollbackError:
            db.rollback()
            cls.commit_to_db(db, model)


class CRUDOperations(DBOperations):

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def update_by_id(cls, db_session: Session, model_id: int,
                     model_changes: any):
        db_model = db_session.get(cls.get_database_model(), model_id)
        if not db_model:
            pass

        data_to_update = model_changes.dict(exclude_unset=True)
        for key, value in data_to_update.items():
            setattr(db_model, key, value)

        db_model = cls.commit_to_db(db=db_session, model=db_model)
        return cls.get_schema_model().from_orm(db_model)

    @classmethod
    def delete(cls, db_session: Session, model: any):
        pass

    @classmethod
    def get_database_model(cls, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def get_schema_model(cls, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def _parse_to_return_model(cls, db_model):
        return cls.get_schema_model().parse_obj(db_model)
