from gzip import open as gzip_open
from csv import DictReader, QUOTE_ALL
from sys import argv
from urllib.request import urlopen

import ijson
import tornado.ioloop

import config
from repository import RepositoryFactory
from server import create_server

if __name__ == '__main__':
    repository_factory = RepositoryFactory(ignore_duplicates=config.IGNORE_DUPLICATES)
    with gzip_open(argv[1], mode='rt') as file:
        # skip header
        next(file)
        repository_factory.add_products(
            DictReader(
                file,
                fieldnames=RepositoryFactory.field_names(),
                quotechar='"',
                quoting=QUOTE_ALL,
                delimiter=',',
                skipinitialspace=True
            )
        )

    with urlopen(argv[2]) as response:
        repository_factory.add_products(ijson.items(response, 'item'))

    if len(argv) > 3:
        port = int(argv[3])
    else:
        port = 8080

    repository = repository_factory.get_repository()
    app = create_server(repository, config.DEFAULT_LENGTH)
    app.listen(port)
    print(f'Server is listening on port {port} with {len(repository)} products')
    tornado.ioloop.IOLoop.current().start()
