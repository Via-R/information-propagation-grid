import asyncio
from grid import Grid


async def main():
    print("Ready")
    field = Grid(21)
    field.place_propagator(2, 2)
    for _ in range(10):
        await field.next()
        field.draw()


if __name__ == "__main__":
    asyncio.run(main())
