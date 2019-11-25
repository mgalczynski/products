import tornado.web


class SingleProductHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ('GET',)

    def initialize(self, repository):
        self._repository = repository

    def get(self, product_id):
        product = self._repository[product_id]
        if product is not None:
            self.finish(product)
        else:
            self.set_status(404, 'Product not found')
            self.finish()


class MultipleProductsHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ('GET',)

    def initialize(self, repository, default_length):
        self._repository = repository
        self._default_length = default_length

    def get(self):
        try:
            length = int(self.get_argument('length', self._default_length, False))
            self.finish({'result': self._repository.n_cheapest(length)})
        except ValueError:
            self.set_status(400, 'Wrong request')


def create_server(repository, default_length):
    arguments = {
        'repository': repository
    }
    return tornado.web.Application([
        (r'/(?P<product_id>\w+)', SingleProductHandler, arguments),
        (r'/', MultipleProductsHandler, {**arguments, 'default_length': default_length})
    ])
