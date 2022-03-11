from sqlalchemy.orm import Session
from app.database.operations import CRUDOperations


class DatabaseInterface(CRUDOperations):

    @classmethod
    def create(cls, db_session: Session, model_data: any):
        db_model = super().create(db_session=db_session, model=model_data)
        return cls.as_schema_model(db_model)

    @classmethod
    def get(cls, db_session: Session, model_id: int):
        db_model = super().get(
            db_session=db_session,
            model=cls.database_model(),
            model_id=model_id,
        )
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
    def database_model(cls, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def schema_model(cls, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def as_schema_model(cls, database_model: any):
        return cls.schema_model().from_orm(database_model)
