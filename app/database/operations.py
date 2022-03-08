from sqlalchemy.orm import Session


def insert(db: Session, data_model):
    db.add(data_model)
    db.commit()
    db.refresh(data_model)
    return data_model

