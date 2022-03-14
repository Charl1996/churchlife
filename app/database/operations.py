from sqlalchemy.orm import Session
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from app.database.exceptions import *


class DBOperations:

    @classmethod
    def commit_to_db(cls, db_session: Session, model=None):
        try:
            if model is None:
                db_session.commit()
            else:
                db_session.add(model)
            db_session.commit()
            db_session.refresh(model)
            return model
        except IntegrityError:
            db_session.rollback()
            raise DuplicateResourceError
        except PendingRollbackError:
            db_session.rollback()
            cls.commit_to_db(db_session, model)
        except Exception:
            db_session.rollback()


class CRUDOperations(DBOperations):

    @classmethod
    def create(cls, db_session: Session, model: any):
        return cls.commit_to_db(db_session=db_session, model=model)

    @classmethod
    def get(cls, db_session: Session, model: any, model_id=None, field=None, value=None):
        if model_id:
            return db_session.get(model, model_id)
        else:
            if not field:
                raise Exception(f'No field provided to query {model} by')
            if not value:
                raise Exception(f'No value provided to query {model} by')

            # I don't like this...
            return eval(f"db_session.query(model).filter(model.{field} == '{value}').first()")

    @classmethod
    def update_by_id(cls, db_session: Session, model: any, model_id: int,
                     model_changes: any):
        db_model = db_session.get(model, model_id)
        if not db_model:
            pass

        data_to_update = model_changes.dict(exclude_unset=True)
        for key, value in data_to_update.items():
            setattr(db_model, key, value)

        return cls.commit_to_db(db_session=db_session, model=db_model)

    @classmethod
    def delete(cls, db_session: Session, model: any, model_id: int):
        instance = db_session.get(model, model_id)
        db_session.delete(instance)
        return cls.commit_to_db(db_session=db_session)
