import adapter.adapter
from interface.movable import IMovable, Vector
from ioc.ioc_container import IoC


class Spaceship:
    pass


def test_adapter_get_methods():
    spaceship = Spaceship()
    adapter_instance = IoC.resolve("adapter", IMovable, spaceship)

    pos = adapter_instance.get_position()
    vel = adapter_instance.get_velocity()

    print(f"get_position() => {pos}")
    print(f"get_velocity() => {vel}")

    assert isinstance(pos, Vector)
    assert isinstance(vel, Vector)


def test_adapter_set_position():
    spaceship = Spaceship()
    adapter_instance = IoC.resolve("adapter", IMovable, spaceship)

    print("Calling set_position...")
    adapter_instance.set_position(Vector(100, 200))


def test_adapter_finish():
    spaceship = Spaceship()
    adapter_instance = IoC.resolve("adapter", IMovable, spaceship)

    print("Calling finish...")
    adapter_instance.finish()
