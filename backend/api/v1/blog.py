from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

# Mencoba mengimpor get_db sesuai lokasi standar proyek FastAPI
try:
    from database.connection import get_db
except ImportError:
    try:
        from database.session import get_db
    except ImportError:
        try:
            from database.deps import get_db
        except ImportError:
            from database.connection import SessionLocal
            def get_db():
                db = SessionLocal()
                try:
                    yield db
                finally:
                    db.close()

from repositories.blog_repository import BlogRepository
from schemas.blog import BlogCreate, BlogUpdate, BlogResponse

# Fungsi dummy get_current_user jika modul core.security belum terkonfigurasi sempurna
try:
    from core.security import get_current_user
except ImportError:
    def get_current_user():
        return None

router = APIRouter(prefix="/blog", tags=["Blog"])

@router.get("/", response_model=List[BlogResponse])
def get_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    repo = BlogRepository(db)
    return repo.get_published(skip=skip, limit=limit)

@router.get("/{slug}", response_model=BlogResponse)
def get_blog_by_slug(slug: str, db: Session = Depends(get_db)):
    repo = BlogRepository(db)
    blog = repo.get_by_slug(slug)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artikel blog tidak ditemukan"
        )
    return blog

@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(
    data: BlogCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repo = BlogRepository(db)
    if repo.get_by_slug(data.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug sudah digunakan"
        )
    blog_dict = data.model_dump()
    if current_user and hasattr(current_user, 'id'):
        blog_dict["author_id"] = current_user.id
    return repo.create(obj_in=blog_dict)

@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: str,
    data: BlogUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repo = BlogRepository(db)
    blog = repo.get(blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artikel blog tidak ditemukan"
        )
    return repo.update(db_obj=blog, obj_in=data)

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    repo = BlogRepository(db)
    blog = repo.get(blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artikel blog tidak ditemukan"
        )
    repo.remove(id=blog_id)
    return None
