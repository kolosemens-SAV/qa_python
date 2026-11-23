import pytest


# ─────────────────────────────────────────────
# add_new_book
# ─────────────────────────────────────────────

def test_add_new_book_adds_book_without_genre(collector):
    """Добавленная книга появляется в словаре, жанр у неё пустой."""
    collector.add_new_book('Гарри Поттер')
    assert collector.get_books_genre() == {'Гарри Поттер': ''}
    assert collector.get_book_genre('Гарри Поттер') == ''


@pytest.mark.parametrize('name, expected', [
    ('A', True),        # 1 символ — минимум
    ('A' * 40, True),   # 40 символов — максимум
    ('A' * 41, False),  # 41 символ — слишком длинно
    ('', False),        # пустая строка
])
def test_add_new_book_length_limits(collector, name, expected):
    """Название добавляется только при длине от 1 до 40 символов."""
    collector.add_new_book(name)
    assert (name in collector.get_books_genre()) is expected


def test_add_new_book_duplicate_not_added(collector):
    """Повторное добавление той же книги не создаёт дубль."""
    collector.add_new_book('Дюна')
    collector.add_new_book('Дюна')
    assert len(collector.get_books_genre()) == 1


# ─────────────────────────────────────────────
# set_book_genre / get_book_genre
# ─────────────────────────────────────────────

def test_set_book_genre_sets_genre(collector):
    """Жанр из списка genre устанавливается и читается обратно."""
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')
    assert collector.get_book_genre('Оно') == 'Ужасы'


@pytest.mark.parametrize('book_name, genre', [
    ('Оно', 'Роман'),                 # жанра нет в списке genre
    ('Неизвестная книга', 'Ужасы'),   # книги нет в books_genre
])
def test_set_book_genre_invalid_data(collector, book_name, genre):
    """Жанр не устанавливается, если жанр недопустим или книги нет в словаре."""
    collector.add_new_book('Оно')
    collector.set_book_genre(book_name, genre)
    assert collector.get_books_genre().get(book_name) in (None, '')


# ─────────────────────────────────────────────
# get_books_with_specific_genre
# ─────────────────────────────────────────────

@pytest.mark.parametrize('genre, expected', [
    ('Ужасы', ['Оно', 'Сияние']),
    ('Комедии', ['Дневник Бриджит Джонс']),
    ('Фантастика', []),   # книг с таким жанром нет
])
def test_get_books_with_specific_genre(collector, genre, expected):
    """Возвращается список книг только с указанным жанром."""
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')
    collector.add_new_book('Сияние')
    collector.set_book_genre('Сияние', 'Ужасы')
    collector.add_new_book('Дневник Бриджит Джонс')
    collector.set_book_genre('Дневник Бриджит Джонс', 'Комедии')
    assert collector.get_books_with_specific_genre(genre) == expected


# ─────────────────────────────────────────────
# get_books_for_children
# ─────────────────────────────────────────────

def test_get_books_for_children_excludes_age_rating(collector):
    """Книги с возрастным рейтингом не попадают в список для детей."""
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')                 # возрастной рейтинг
    collector.add_new_book('Король Лев')
    collector.set_book_genre('Король Лев', 'Мультфильмы')    # без рейтинга
    collector.add_new_book('Без жанра')                       # жанр не задан
    assert collector.get_books_for_children() == ['Король Лев']


# ─────────────────────────────────────────────
# add_book_in_favorites
# ─────────────────────────────────────────────

def test_add_book_in_favorites_success_and_no_duplicate(collector):
    """Книга добавляется в избранное, повторно — не добавляется."""
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    collector.add_book_in_favorites('Дюна')
    assert collector.get_list_of_favorites_books() == ['Дюна']


def test_add_book_in_favorites_requires_book_in_dict(collector):
    """Книгу, которой нет в books_genre, нельзя добавить в избранное."""
    collector.add_book_in_favorites('Несуществующая книга')
    assert collector.get_list_of_favorites_books() == []


# ─────────────────────────────────────────────
# delete_book_from_favorites
# ─────────────────────────────────────────────

@pytest.mark.parametrize('delete_name, expected', [
    ('Дюна', []),                 # книга есть в избранном — удалится
    ('Другая книга', ['Дюна']),   # книги нет в избранном — список не изменится
])
def test_delete_book_from_favorites(collector, delete_name, expected):
    """Удаление из избранного работает только для существующей там книги."""
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    collector.delete_book_from_favorites(delete_name)
    assert collector.get_list_of_favorites_books() == expected


# ─────────────────────────────────────────────
# get_book_genre
# ─────────────────────────────────────────────

def test_get_book_genre_returns_genre(collector):
    """get_book_genre возвращает жанр книги по её имени."""
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Ужасы')
    assert collector.get_book_genre('Оно') == 'Ужасы'


# ─────────────────────────────────────────────
# get_books_genre
# ─────────────────────────────────────────────

def test_get_books_genre_returns_books_dict(collector):
    """get_books_genre возвращает текущий словарь books_genre."""
    collector.add_new_book('Дюна')
    collector.set_book_genre('Дюна', 'Фантастика')
    assert collector.get_books_genre() == {'Дюна': 'Фантастика'}


# ─────────────────────────────────────────────
# get_list_of_favorites_books
# ─────────────────────────────────────────────

def test_get_list_of_favorites_books_returns_favorites(collector):
    """get_list_of_favorites_books возвращает список избранных книг."""
    collector.add_new_book('Дюна')
    collector.add_book_in_favorites('Дюна')
    assert collector.get_list_of_favorites_books() == ['Дюна']