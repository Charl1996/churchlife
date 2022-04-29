from sqlalchemy.exc import PendingRollbackError, IntegrityError
from app.database.exceptions import *
from fastapi_sqlalchemy import db


class DBOperations:

    @classmethod
    def commit_to_db(cls, model=None):
        try:
            if model is None:
                db.session.commit()
            else:
                db.session.add(model)
            db.session.commit()
            db.session.refresh(model)
            return model
        except IntegrityError:
            db.session.rollback()
            raise DuplicateResourceError
        except PendingRollbackError:
            db.session.rollback()
            cls.commit_to_db(db.session, model)
        except Exception:
            db.session.rollback()


class CRUDOperations(DBOperations):

    @classmethod
    def create(cls, model: any):
        return cls.commit_to_db(model=model)

    @classmethod
    def get(cls, model: any, model_id=None, field=None, value=None, criteria=None, count=False, get_all=False):
        if model_id:
            result = db.session.get(model, model_id)
        elif criteria:
            criteria_string = cls._get_criteria_string(criteria)

            if get_all:
                result = eval(f"db.session.query(model).filter({criteria_string})")
            else:
                # I don't like this...
                action = 'first'
                if count:
                    action = 'count'
                result = eval(f"db.session.query(model).filter({criteria_string}).{action}()")
        else:
            if not field:
                raise Exception(f'No field provided to query {model} by')
            if not value:
                raise Exception(f'No value provided to query {model} by')

            # I don't like this...
            action = 'first'
            if count:
                action = 'count'
            result = eval(f"db.session.query(model).filter(model.{field} == '{value}').{action}()")

        if not result:
            return 0 if count else None
        return result

    @classmethod
    def update_by_id(cls, model: any, model_id: int,
                     model_changes: any):
        db_model = db.session.get(model, model_id)
        if not db_model:
            pass

        data_to_update = model_changes.dict(exclude_unset=True)
        for key, value in data_to_update.items():
            setattr(db_model, key, value)

        return cls.commit_to_db(model=db_model)

    @classmethod
    def delete(cls, model: any, model_id: int):
        instance = db.session.get(model, model_id)
        db.session.delete(instance)
        return cls.commit_to_db()

    @classmethod
    def delete_where(cls, model: any, criteria: dict):
        criteria_string = cls._get_criteria_string(criteria)
        return eval(f"db.session.query(model).filter({criteria_string}).delete()")

    @classmethod
    def _get_criteria_string(cls, criteria: dict) -> str:
        def criterion_string(field_, value_):
            return f"model.{field_} == '{value_}'"

        criteria_string = ''
        for field, value in criteria.items():
            if criteria_string == '':
                criteria_string = criterion_string(field, value)
            else:
                criteria_string = f'{criteria_string}, {criterion_string(field, value)}'
        return criteria_string
