import asyncio
import contextvars

async_session = contextvars.ContextVar("async_session")


async def get_async_session():
    async with async_session_maker() as session:
        try:
            _token = async_session.set(session)
            yield session
        finally:
            async_session.reset(_token)


if __name__ == "__main__":
    asyncio.run(get_async_session())
