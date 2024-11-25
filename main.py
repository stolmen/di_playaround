from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from services.render import RenderService
from container import Container


@inject
def print_data(
    render_service: RenderService = Provide[Container.render_service],
):
    if render_service.is_stale:
        render_service.refresh_data()
    data = render_service.render_data()
    print(data)


def main():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    print_data()
    print(container.config.asdf.qewr)  # what is this and how do I use it?


if __name__ == "__main__":
    main()
