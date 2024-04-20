from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


async def get_async_session(
        engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """
    Despite I was supposed to use method `get_async_session`, which returns
    AsyncSession sqlalchemy object to interact with db,
    I decided to create a session inside my UserService because the
    sqlalchemy documentation says: 'The Session is a mutable, stateful
    object that represents a single database transaction. An instance of
    Session therefore cannot be shared among concurrent threads or
    asyncio tasks without careful synchronization'.

    For more info visit:
    https://docs.sqlalchemy.org/en/20/orm/session_basics.html#is-the-session-thread-safe-is-asyncsession-safe-to-share-in-concurrent-tasks
    """
    return async_sessionmaker(engine, expire_on_commit=False)
