from sqlalchemy.orm import Session


def insert(func):
    def wrapper(db: Session, *args, **kwargs):
        data_model = func(*args, **kwargs)
        db.add(data_model)
        db.commit()
        db.refresh(data_model)
        return data_model

    return wrapper
