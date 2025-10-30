from ..persistence.catalog import DataCatalog
from ..logging.ConsoleLogger import ConsoleLogger

class OrionContext:
    def __init__(self, catalog: DataCatalog, logger=None):
        self.catalog = catalog
        self.logger = logger or ConsoleLogger()
