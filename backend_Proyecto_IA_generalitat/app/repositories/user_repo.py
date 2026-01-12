from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

class UserRepo:
    def get_by_email(self, db: Session, email: str) -> User | None:
        """Retrieve a user by email address."""
        return db.scalar(select(User).where(User.email == email))

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        """Retrieve a user by ID."""
        return db.get(User, user_id)

    def create(self, db: Session, email: str, password_hash: str, nombre: str) -> User:
        """Create a new user in the database."""
        user = User(email=email, password_hash=password_hash, nombre=nombre)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

user_repo = UserRepo()
