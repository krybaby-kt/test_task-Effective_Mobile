import asyncio
from database import init_models, fill_database
import uvicorn


async def main():
    await init_models()
    await fill_database()

    web_api_config = uvicorn.Config(
        app="web_api:app",
        log_level="debug",
        host="localhost",
        port=8000,
        reload=False,
        workers=4,
        use_colors=True,
    )
    web_api_server = uvicorn.Server(web_api_config)

    await asyncio.gather(
        web_api_server.serve(),
    )

    
if __name__ == "__main__":
    asyncio.run(main())