from math import inf


def bool_factory(input_value):
    if isinstance(input_value, bool):
        return input_value
    return {
        'yes': True,
        'y': True,
        'n': False,
        'no': False,
    }[input_value.lower()]


class DuplicatedProductError(ValueError):
    def __init__(self, product_id):
        super().__init__(f'Duplicated product id {product_id}')


class RepositoryFactory:
    _fields = [
        ('id', str),
        ('name', str),
        ('brand', str),
        ('retailer', str),
        ('price', float),
        ('in_stock', bool_factory),
    ]

    def __init__(self, *, ignore_duplicates):
        self._ignore_duplicates = ignore_duplicates
        self._products_dict = {}

    @classmethod
    def _convert_product(cls, product):
        for name, factory in cls._fields:
            value = product.get(name)
            yield name, factory(value) if value else None

    @classmethod
    def _convert(cls, products):
        for product in products:
            yield dict(cls._convert_product(product))

    @classmethod
    def field_names(cls):
        return [name for name, _ in cls._fields]

    def add_products(self, products):
        for product in self._convert(products):
            product_id = product['id']
            if not self._ignore_duplicates and product_id in self._products_dict:
                raise DuplicatedProductError(product_id)
            self._products_dict[product_id] = product

    def get_repository(self):
        return Repository(self._products_dict)


class RepositoryArgumentError(ValueError):
    pass


class Repository:
    def __init__(self, products):
        self._products_dict = dict(products)
        self._products_sorted_by_price = sorted(self._products_dict.values(),
                                                key=lambda product: product['price'] or inf)

    def __getitem__(self, item):
        return self._products_dict.get(item)

    def __len__(self):
        return len(self._products_dict)

    def n_cheapest(self, n):
        if n < 1:
            raise RepositoryArgumentError(f'Not valid length {n}')
        return self._products_sorted_by_price[:n]
