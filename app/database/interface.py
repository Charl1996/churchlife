from sqlalchemy.orm import Session
from app.database.operations import CRUDOperations
from app.database.exceptions import ResourceNotFound


class DatabaseInterface(CRUDOperations):

    @classmethod
    def create(cls, model_data: any):
        db_model = super().create(model=model_data)
        return cls.as_schema_model(db_model)

    @classmethod
    def get(
            cls,
            model_id: int,
            raise_error=False,
    ):
        db_model = super().get(
            model=cls.database_model(),
            model_id=model_id,
        )

        if raise_error and db_model is None:
            raise ResourceNotFound

        return cls.as_schema_model(db_model)

    @classmethod
    def get_by(
            cls,
            model=None,
            field=None,
            value=None,
            schema=None,
            raise_error=False,
            criteria=None,
    ):
        if model is None:
            model = cls.database_model()
        db_model = super().get(
            model=model,
            field=field,
            value=value,
            criteria=criteria,
        )

        if raise_error and db_model is None:
            raise ResourceNotFound

        if schema:
            return cls.as_schema_model(db_model, schema=schema)
        return cls.as_schema_model(db_model)

    @classmethod
    def get_all_by(
            cls,
            model=None,
            field=None,
            value=None,
            schema=None,
            raise_error=False,
            criteria=None,
    ):
        if model is None:
            model = cls.database_model()
        db_models = super().get(
            model=model,
            field=field,
            value=value,
            criteria=criteria,
            get_all=True,
        )

        if raise_error and db_models is None:
            raise ResourceNotFound

        results = []
        for db_model in db_models:
            if schema:
                results.append(cls.as_schema_model(db_model, schema=schema))
            else:
                results.append(cls.as_schema_model(db_model))
        return results

    @classmethod
    def get_count(
            cls,
            field=None,
            value=None,
            model=None,
            criteria=None,
    ):
        db_count = super().get(
            model=model or cls.database_model(),
            field=field,
            value=value,
            criteria=criteria,
            count=True,
        )

        return db_count

    @classmethod
    def update_by_id(cls, model_id: int, model_changes: any):
        db_model = super().update_by_id(
            model=cls.database_model(),
            model_id=model_id,
            model_changes=model_changes,
        )
        return cls.as_schema_model(db_model)

    @classmethod
    def delete(cls, model: any, model_id: int):
        result = super().delete(
            model=model or cls.database_model(),
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


class DatabaseInterfaceWrapper(DatabaseInterface):

    @classmethod
    def create(cls, data: any):
        create_schema = cls.create_schema_model()(**data)
        db_model = cls.create_model(create_schema)
        schema_model = super().create(model_data=db_model)
        return cls.init_class_instance(schema_model)

    @classmethod
    def get(cls, model_id: int):
        schema_model = super().get(model_id=model_id)
        if not schema_model:
            return None
        return cls.init_class_instance(schema_model)

    @classmethod
    def get_by_domain(cls, domain: str):
        schema_model = super().get_by(field="domain", value=domain)
        if not schema_model:
            return None
        return cls.init_class_instance(schema_model)

    @classmethod
    def init_class_instance(cls):
        """
        This method should initialize the class instance associated
        with the database model
        """
        raise NotImplementedError

    @classmethod
    def create_model(cls, data):
        """
        This method should implement the specific implementation used
        to create the model
        """
        raise NotImplementedError
