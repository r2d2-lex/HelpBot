from google_images_search import GoogleImagesSearch
from io import BytesIO
from config import GOOGLE_SEARCH_IMAGE_API, GOOGLE_SEARCH_IMAGE_CX, logging

QUERY_FIELD = 'q'
NUM_FIELD = 'num'


def google_search_image(query: str, num_images=10):
    gis = GoogleImagesSearch(GOOGLE_SEARCH_IMAGE_API, GOOGLE_SEARCH_IMAGE_CX)
    gis.search({QUERY_FIELD: query, NUM_FIELD: num_images})
    for image in gis.results():
        my_bytes_io = BytesIO()
        my_bytes_io.seek(0)
        raw_image_data = image.get_raw_data()
        image.copy_to(my_bytes_io, raw_image_data)
        image.copy_to(my_bytes_io)
        my_bytes_io.seek(0)
        yield my_bytes_io
        my_bytes_io.close()
