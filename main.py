from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from services import DataService
from container import Container

import rich

# providers - compose these into a container

# whats the difference between a singleton and a factory?


@inject
def print_data(
    data_service: DataService = Provide[Container.data_service],
):
    if data_service.is_stale:
        data_service.refresh_data()
    data = data_service.render_data()
    print(data)


def main():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    print_data()
    print(container.config.asdf.qewr)  # what is this and how do I use it?


if __name__ == "__main__":
    main()
