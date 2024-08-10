from os import getenv

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import String, BigInteger, Column
from sqlalchemy.ext.asyncio import (async_sessionmaker,
									create_async_engine,
									AsyncAttrs)
from sqlalchemy.orm import DeclarativeBase

load_dotenv(find_dotenv())

IP = getenv('IP')
PGUSER = getenv('PGUSER')
PGPASSWORD = getenv('PGPASSWORD')
DATABASE = getenv('DATABASE')

POSTGRES_URL = f'postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'
engine = create_async_engine(POSTGRES_URL, echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
	pass

class User(Base):
	__tablename__ = "users"

	user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
	username = Column(String(35), nullable=True)
	fullname = Column(String(100), nullable=True)
	send = Column(BigInteger, nullable=True)


async def async_database_create():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)