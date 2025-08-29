from src.core.di.containers import Container

container = Container()


def init_container():
    """Initialize the dependency injection container"""
    container.init_resources()
    return container


def shutdown_container():
    """Shutdown the dependency injection container"""
    container.shutdown_resources()

__all__ = ['container', 'init_container', 'shutdown_container']