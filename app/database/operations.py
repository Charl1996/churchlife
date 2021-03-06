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
            try:
                db.session.refresh(model)
                return model
            except Exception:
                return
        except IntegrityError:
            db.session.rollback()
            raise DuplicateResourceError
        except PendingRollbackError:
            db.session.rollback()
            cls.commit_to_db(db.session, model)
        except Exception:
            db.session.rollback()
            raise


class CRUDOperations(DBOperations):

    @classmethod
    def create(cls, model: any, transaction=False):
        if transaction:
            db.session.add(model)
        else:
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

        def criterion_string_with_operator(field_, value_, operator):
            return f"model.{field_} {operator} '{value_}'"

        criteria_string = ''
        for field, value in criteria.items():
            if criteria_string == '':
                if type(value) != dict:
                    criteria_string = criterion_string(field, value)
                elif type(value) == dict:
                    if value.get('logic'):
                        logical_operation = value['logic']  # Currently only supports AND
                        logical_operation_criteria = value['criteria']

                        logical_criteria_string = ''
                        for logical_criterion in logical_operation_criteria:
                            op = logical_criterion['operator']
                            v = logical_criterion['value']
                            if logical_criteria_string:
                                logical_criteria_string = f'{logical_criteria_string}, {criterion_string_with_operator(field, v, op)}'
                            else:
                                logical_criteria_string = f'{criterion_string_with_operator(field, v, op)}'
                        criteria_string = logical_criteria_string
                    else:
                        v = value['value']
                        op = value['operator']
                        criteria_string = f'{criterion_string_with_operator(field, v, op)}'
            else:
                if type(value) != dict:
                    criteria_string = f'{criteria_string}, {criterion_string(field, value)}'
                elif type(value) == dict:
                    if value.get('logic'):
                        logical_operation = value['logic']  # Currently only supports AND
                        logical_operation_criteria = value['criteria']

                        logical_criteria_string = ''
                        for logical_criterion in logical_operation_criteria:
                            op = logical_criterion['operator']
                            v = logical_criterion['value']
                            if logical_criteria_string:
                                logical_criteria_string = f'{logical_criteria_string}, {criterion_string_with_operator(field, v, op)}'
                            else:
                                logical_criteria_string = f'{criterion_string_with_operator(field, v, op)}'
                        criteria_string = f'{criteria_string}, {logical_criteria_string}'
                    else:
                        v = value['value']
                        op = value['operator']
                        criteria_string = f'{criterion_string_with_operator(field, v, op)}'

        return criteria_string
