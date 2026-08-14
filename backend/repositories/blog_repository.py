from sqlalchemy.orm import Session
from models.blog import Blog

class BlogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, blog_id: str) -> Blog | None:
        return self.db.query(Blog).filter(Blog.id == blog_id).first()

    def get_by_slug(self, slug: str) -> Blog | None:
        return self.db.query(Blog).filter(Blog.slug == slug).first()

    def get_published(self, skip: int = 0, limit: int = 20):
        return (
            self.db.query(Blog)
            .filter(Blog.is_published == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, obj_in: dict) -> Blog:
        db_obj = Blog(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Blog, obj_in) -> Blog:
        update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, "model_dump") else obj_in
        for field, value in update_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, id: str) -> Blog | None:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
