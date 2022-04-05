from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextvars import ContextVar
from sqlalchemy.orm import sessionmaker
from application.server import app
from application.models.models import Base

_base_model_session_ctx = ContextVar("session")

bind = create_async_engine("mysql+aiomysql://vidai:21112000a@localhost/sanic", echo=True)

@app.middleware("request")
async def inject_session(request):
    request.ctx.session = sessionmaker(bind, AsyncSession, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)
    async with bind.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()