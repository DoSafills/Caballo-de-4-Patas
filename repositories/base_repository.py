from typing import Type, List
from sqlalchemy.orm import Session

class BaseRepository:
    """Repositorio genérico con operaciones CRUD básicas."""
    def __init__(self, session: Session, model: Type):
        self.session = session
        self.model = model

    def add(self, **data):
        obj = self.model(**data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get(self, **filters):
        return self.session.query(self.model).filter_by(**filters).first()

    def get_all(self) -> List:
        return self.session.query(self.model).all()

    def update(self, obj, **data):
        for key, value in data.items():
            setattr(obj, key, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()
