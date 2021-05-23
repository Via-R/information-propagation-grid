import asyncio
from lattice import Lattice


async def main():
    print("Ready")
    field = Lattice(21)


if __name__ == "__main__":
    asyncio.run(main())
