import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import unittest
import asyncio
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from app import create_app
from db import db, async_session
from models import User


class TestUserModel(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.app = create_app()  ## create_app(config_name='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db
        self.async_session = async_session

        self.session = self.async_session()

        ## async with self.async_session() as session:
        ##     async with session.begin():
        ##         await session.run_sync(self.db.create_all)

        self.sample_user_data = {"username": "testuser", "password": "password123"}

    async def asyncTearDown(self):
        ## async with self.async_session() as session:
        ##     async with session.begin():
        ##         await session.run_sync(self.db.drop_all)

        # Roll back the transaction to discard changes
        await self.session.rollback()
        await self.session.close()

        if self.app_context is not None:
            self.app_context.pop()

    async def test_user_operations(self):
        async with self.session.begin():
            user = User(**self.sample_user_data)
            self.session.add(user)
            await self.session.commit()

        async with self.session.begin():
            await self.session.refresh(user)

        async with self.session.begin():
            created_user = await self.session.get(User, user.id)
            self.assertIsNotNone(created_user)
            self.assertEqual(created_user.username, "testuser")
            self.assertTrue(created_user.password)

        async with self.session.begin():
            stmt = select(User).where(
                User.username == "testuser",
            )
            result = await self.session.execute(stmt)
            queried_user = result.scalar_one_or_none()
            print(f"queried_user={queried_user}")
            self.assertIsNotNone(queried_user)
            self.assertEqual(queried_user.username, "testuser")

        async with self.session.begin():
            user.username = "updateduser"
            await self.session.commit()

        async with self.session.begin():
            updated_user = await self.session.get(User, user.id)
            self.assertEqual(updated_user.username, "updateduser")

        async with self.session.begin():
            updated_user.soft_delete()
            await self.session.commit()

        async with self.session.begin():
            stmt = select(User).where(
                User.id == user.id,
                User.username == "updateduser",
                User.deleted_at.isnot(None),
            )
            result = await self.session.execute(stmt)
            deleted_user = result.scalar_one_or_none()
            self.assertIsNotNone(deleted_user.deleted_at)

        async with self.session.begin():
            stmt = select(User).where(
                User.id == user.id,
                User.username == "updateduser",
                User.deleted_at.is_(None),
            )
            result = await self.session.execute(stmt)
            active_user = result.scalar_one_or_none()
            self.assertIsNone(active_user)

        async with self.session.begin():
            await self.session.delete(updated_user)
            await self.session.commit()

        async with self.session.begin():
            deleted_user = await self.session.get(User, user.id)
            self.assertIsNone(deleted_user)

    @unittest.skip("This test is disabled by default")
    async def test_create_user(self):
        async with self.session.begin():
            user = User(**self.sample_user_data)
            self.session.add(user)
            await self.session.commit()

        async with self.session.begin():
            await self.session.refresh(user)

        async with self.session.begin():
            created_user = await self.session.get(User, user.id)

        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "testuser")
        self.assertTrue(created_user.password)

    @unittest.skip("This test is disabled by default")
    async def test_query_user(self):
        async with self.session.begin():
            user = User(**self.sample_user_data)
            self.session.add(user)
            await self.session.commit()

        async with self.session.begin():
            stmt = select(User).where(
                User.username == "testuser",
            )
            result = await self.session.execute(stmt)
            queried_user = result.scalar_one_or_none()
            print(f"queried_user={queried_user}")
            self.assertIsNotNone(queried_user)
            self.assertEqual(queried_user.username, "testuser")

    @unittest.skip("This test is disabled by default")
    async def test_update_user(self):
        async with self.session.begin():
            user = User(**self.sample_user_data)
            self.session.add(user)
            await self.session.commit()

        async with self.session.begin():
            user.username = "updateduser"
            await self.session.commit()

        async with self.session.begin():
            updated_user = await self.session.get(User, user.id)
            self.assertEqual(updated_user.username, "updateduser")

    @unittest.skip("This test is disabled by default")
    async def test_soft_delete_user(self):
        async with self.session.begin():
            user = User(**self.sample_user_data)
            self.session.add(user)
            await self.session.commit()

        async with self.session.begin():
            await self.session.refresh(user)

        async with self.session.begin():
            user.soft_delete()
            await self.session.commit()

        async with self.session.begin():
            stmt = select(User).where(
                User.id == user.id,
                User.username == "testuser",
                User.deleted_at.isnot(None),
            )
            result = await self.session.execute(stmt)
            deleted_user = result.scalar_one_or_none()
            self.assertIsNotNone(deleted_user.deleted_at)

        async with self.session.begin():
            stmt = select(User).where(
                User.id == user.id,
                User.username == "testuser",
                User.deleted_at.is_(None),
            )
            result = await self.session.execute(stmt)
            active_user = result.scalar_one_or_none()
            self.assertIsNone(active_user)

    @unittest.skip("This test is disabled by default")
    async def test_delete_user(self):
        async with self.session.begin():
            user = User(**self.sample_user_data)
            self.session.add(user)
            await self.session.commit()

        async with self.session.begin():
            await self.session.refresh(user)

        async with self.session.begin():
            await self.session.delete(user)
            await self.session.commit()

        async with self.session.begin():
            deleted_user = await self.session.get(User, user.id)
            self.assertIsNone(deleted_user)


if __name__ == "__main__":
    unittest.main()
