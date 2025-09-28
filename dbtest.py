import asyncio
from prisma import Prisma

async def main() -> None:
    prisma = Prisma()
    await prisma.connect()

    # write your queries here
    user = await prisma.user.create(
        data={
            'name': 'Robert',
            'email': 'robert_1@craigie.dev'
        },
    )

    users = await prisma.user.find_many()
    print(users)

    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())