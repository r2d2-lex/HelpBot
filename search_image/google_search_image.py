from google_images_search import GoogleImagesSearch
from io import BytesIO
from config import GOOGLE_SEARCH_IMAGE_API, GOOGLE_SEARCH_IMAGE_CX, logging

QUERY_FIELD = 'q'
NUM_FIELD = 'num'
PAGE_COUNT_IMAGES = 10

user_context = dict(
    search_continue=False,
    search_context=None,
)


def google_next_search():
    user_context['search_continue'] = True


def google_new_search():
    user_context['search_continue'] = False


def google_search_image(query: str, num_images=PAGE_COUNT_IMAGES):
    if user_context.get('search_continue', False):
        logging.info('Next search pages...')
        gis = user_context.get('search_context', None)
        gis.next_page()
    else:
        logging.info(f'New search with {query}...')
        gis = GoogleImagesSearch(GOOGLE_SEARCH_IMAGE_API, GOOGLE_SEARCH_IMAGE_CX)
        gis.search({
            QUERY_FIELD: query,
            NUM_FIELD: num_images
        })
        user_context['search_context'] = gis

    for image in gis.results():
        my_bytes_io = BytesIO()
        my_bytes_io.seek(0)
        raw_image_data = image.get_raw_data()
        image.copy_to(my_bytes_io, raw_image_data)
        image.copy_to(my_bytes_io)
        my_bytes_io.seek(0)
        yield my_bytes_io
        my_bytes_io.close()
