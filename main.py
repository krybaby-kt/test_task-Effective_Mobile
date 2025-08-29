import asyncio
from database import init_models


async def main():
    await init_models()
    
if __name__ == "__main__":
    asyncio.run(main())