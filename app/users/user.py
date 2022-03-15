from sqlalchemy.orm import Session
from app.database.interface import DatabaseInterface

from app.database import User as UserModel
from app.database import OrganisationsUsers
from app.users.user_schema import (
    UserCreate,
    UserLogin,
    User as UserSchema,
    UserOrganisationView,
)
from app.organisations import Organisation
from app.security.utils import (
    hash_string,
    check_password
)
from app.security.auth import sign_jwt


class User(DatabaseInterface):

    # Make sure all these db_session's are closed after each request
    db_session: Session
    user: UserSchema

    @classmethod
    def database_model(cls):
        return UserModel

    @classmethod
    def schema_model(cls):
        return UserSchema

    @classmethod
    def create(cls, db_session: Session, data: dict):
        user_create = UserCreate(**data)

        user_model = UserModel(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            email=user_create.email,
            password=hash_string(user_create.password),
        )
        user_schema = super().create(db_session=db_session, model_data=user_model)
        return cls(db_session=db_session, user=user_schema)

    @classmethod
    def get(cls, db_session: Session, user_id: int):
        user_schema = super().get(db_session=db_session, model_id=user_id)
        return cls(db_session=db_session, user=user_schema)

    @classmethod
    def get_by_email(cls, db_session: Session, email: str):
        user_schema = super().get_by(db_session=db_session, field="email", value=email)
        return cls(db_session=db_session, user=user_schema)

    @classmethod
    def delete(cls, db_session: Session, user_id: int):
        # Do user specific stuff here
        # - Remove OrganisationUser
        super().delete(db_session=db_session, model_id=user_id)

    @classmethod
    def check_credentials(cls, db_session: Session, email: str, password: str) -> bool:
        user = super().get_by(db_session=db_session, field='email', value=email, schema=UserLogin, raise_error=True)
        return check_password(password=password, hashed_password=user.password)

    @classmethod
    def log_in(cls, db_session: Session, email: str, password: str):
        if not cls.check_credentials(db_session, email, password):
            return None

        user = cls.get_by_email(db_session, email)
        if not user:
            return None

        return sign_jwt({'user_email': user.fields.email})  # need to use uuid

    def __init__(self, db_session: Session, user: UserSchema):
        self.db_session = db_session
        self.user = user

    @property
    def fields(self) -> UserSchema:
        return self.user

    @property
    def organisations(self):
        return [UserOrganisationView.from_orm(org) for org in self.fields.organisations]

    def belongs_to_domain(self, domain: str) -> bool:
        org = Organisation.get_by_domain(db_session=self.db_session, domain=domain)
        if not org:
            return False

        organisation_user = self.db_session.query(OrganisationsUsers)\
            .filter(OrganisationsUsers.user_id == self.fields.id and OrganisationsUsers.organisation_id == org.id)

        return True if organisation_user else False
