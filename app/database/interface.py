from sqlalchemy.orm import Session
from app.database.operations import CRUDOperations
from app.database.exceptions import ResourceNotFound


class DatabaseInterface(CRUDOperations):

    @classmethod
    def create(cls, db_session: Session, model_data: any):
        db_model = super().create(db_session=db_session, model=model_data)
        return cls.as_schema_model(db_model)

    @classmethod
    def get(cls, db_session: Session, model_id: int, raise_error=False):
        db_model = super().get(
            db_session=db_session,
            model=cls.database_model(),
            model_id=model_id,
        )

        if raise_error and db_model is None:
            raise ResourceNotFound

        return cls.as_schema_model(db_model)

    @classmethod
    def get_by(cls, db_session: Session, field: str, value: any, schema=None, raise_error=False):
        db_model = super().get(
            db_session=db_session,
            model=cls.database_model(),
            field=field,
            value=value,
        )

        if raise_error and db_model is None:
            raise ResourceNotFound

        if schema:
            return cls.as_schema_model(db_model, schema=schema)
        return cls.as_schema_model(db_model)

    @classmethod
    def update_by_id(cls, db_session: Session, model_id: int, model_changes: any):
        db_model = super().update_by_id(
            db_session=db_session,
            model=cls.database_model(),
            model_id=model_id,
            model_changes=model_changes,
        )
        return cls.as_schema_model(db_model)

    @classmethod
    def delete(cls, db_session: Session, model_id: int):
        result = super().delete(
            db_session=db_session,
            model=cls.database_model(),
            model_id=model_id
        )
        return result

    @classmethod
    def database_model(cls, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def schema_model(cls, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def as_schema_model(cls, database_model: any, schema=None):
        if not database_model:
            return None

        if schema is not None:
            return schema.from_orm(database_model)
        return cls.schema_model().from_orm(database_model)
