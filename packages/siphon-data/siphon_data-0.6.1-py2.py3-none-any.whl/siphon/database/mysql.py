from typing import AsyncGenerator, Dict, List, Optional, Tuple, Union

import aiomysql as mysql

from siphon.database.config import DatabaseConfig


class MySQLConfig(DatabaseConfig):
    port: int = 3306
    db: Optional[str]


class AioMySQL:
    def __init__(
        self,
        config: MySQLConfig,
        cursor_class: mysql.Cursor = mysql.SSDictCursor,
        min_size: int = 1,
        max_size: int = 10,
    ):
        self.pool = None
        self.config = config
        self.cursor_class = cursor_class
        self.min_size = min_size
        self.max_size = max_size

    async def setup_pool(self):
        self.pool = await mysql.create_pool(
            host=self.config.host.get_secret_value(),
            user=self.config.user.get_secret_value(),
            password=self.config.password.get_secret_value(),
            db=self.config.db,
            port=self.config.port,
            minsize=self.min_size,
            maxsize=self.max_size,
        )

    async def __aenter__(self):
        await self.setup_pool()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_pool()

    async def read(self, query: str, params: Tuple = None) -> AsyncGenerator:
        async with self.pool.acquire() as conn:  # type: ignore
            async with conn.cursor(self.cursor_class) as cur:
                await cur.execute(query, params)
                async for row in cur:
                    yield row

    async def read_all(self, query: str, params: Tuple = None) -> List[Dict]:
        rows = []
        async for row in self.read(query, params):
            rows.append(row)
        return rows

    async def write(self, stmt: str, params: Union[Tuple, str, int]) -> None:
        async with self.pool.acquire() as conn:  # type: ignore
            async with conn.cursor() as cur:
                await cur.executemany(stmt, params)
            await conn.commit()

    async def commit(self, stmt: str):
        async with self.pool.acquire() as conn:  # type: ignore
            async with conn.cursor() as cur:
                await cur.execute(stmt)
            await conn.commit()

    async def close_pool(self):
        self.pool.close()
        await self.pool.wait_closed()
