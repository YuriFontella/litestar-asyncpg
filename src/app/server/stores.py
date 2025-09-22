from litestar.stores.memory import MemoryStore

memory_store = MemoryStore()


def default_store(name: str) -> MemoryStore:
    return memory_store
