from books.models import Books

menu = [
    {'title': 'Главная страница', 'url_name': 'home'},
    {'title': 'Каталог', 'url_name': 'catalog'},
    {'title': 'Корзина'},
]


class DataMixin:
    paginate_by = 6
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context.update(kwargs)
        return context


