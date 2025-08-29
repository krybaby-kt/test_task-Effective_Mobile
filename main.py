import asyncio
from database import init_models, fill_database


async def main():
    await init_models()
    await fill_database()

    
if __name__ == "__main__":
    asyncio.run(main())