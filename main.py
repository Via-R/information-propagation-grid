import asyncio
from grid import Grid


async def main():
    print("Ready")
    side_size = 20
    field = Grid(side_size+1)
    field.place_propagator(side_size // 2, side_size // 2)
    # field.matrix[0][0].credibility_evaluator.draw_graders()
    # return
    for _ in range(int(side_size * 1.7)):
        await field.next()
        field.draw()


if __name__ == "__main__":
    asyncio.run(main())
