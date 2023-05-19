from google_images_search import GoogleImagesSearch
from io import BytesIO
from services import UserState, users_context
from config import GOOGLE_SEARCH_IMAGE_API, GOOGLE_SEARCH_IMAGE_CX, logging

QUERY_FIELD = 'q'
NUM_FIELD = 'num'
PAGE_COUNT_IMAGES = 10


def google_next_search(userid: int):
    user_state = users_context.get(userid)
    user_state.search_continue = True
    users_context.update({userid: user_state})


def google_new_search(userid: int):
    user_state = UserState(user_id=userid, search_context=None, search_continue=False)
    users_context.update({userid: user_state})


def google_search_image(query: str, userid: int, num_images=PAGE_COUNT_IMAGES):
    user_state = users_context.get(userid)
    if user_state.search_continue:
        logging.info('Next search pages...')
        gis = user_state.search_context
        gis.next_page()
    else:
        logging.info(f'New search with {query}...')
        gis = GoogleImagesSearch(GOOGLE_SEARCH_IMAGE_API, GOOGLE_SEARCH_IMAGE_CX)
        gis.search({
            QUERY_FIELD: query,
            NUM_FIELD: num_images
        })
        users_context.update({userid: UserState(user_id=userid, search_continue=False, search_context=gis)})

    for image in gis.results():
        my_bytes_io = BytesIO()
        my_bytes_io.seek(0)
        raw_image_data = image.get_raw_data()
        image.copy_to(my_bytes_io, raw_image_data)
        image.copy_to(my_bytes_io)
        my_bytes_io.seek(0)
        yield my_bytes_io
        my_bytes_io.close()
