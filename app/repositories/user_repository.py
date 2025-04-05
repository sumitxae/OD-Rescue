from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.user_model import User
from ..utils.handler_error import handle_db_exceptions

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @handle_db_exceptions(rollback_on_fail=True)
    async def get_user_by_id(self, user_id: int):
        stmt = select(User).options(joinedload(User.role)).where(User.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    @handle_db_exceptions(rollback_on_fail=True)
    async def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    @handle_db_exceptions(rollback_on_fail=True)
    async def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    @handle_db_exceptions(rollback_on_fail=True)
    async def create_user(self, user_data: dict):
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user  
    
    @handle_db_exceptions(rollback_on_fail=True)
    async def update_user(self, user_id: int, update_data: dict):
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(**update_data)
            .returning(User)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()  
        return result.scalars().first()
