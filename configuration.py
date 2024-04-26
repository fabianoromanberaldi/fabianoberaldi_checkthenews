BROWSER = 'headlessfirefox'
SEARCH_PHRASE = 'Dengue'
MONTHS = 1
TIMEOUT_IN_SECONDS = 60
AUTO_CLOSE = True
DOWNLOAD_IMAGES = True
ATTEMPTS = 2

WORKBOOK_PATH = './output/nyt_news.xlsx'
SHEET_NAME = 'news'
SHEET_COLUMNS = ['date',
                 'search_phrase',
                 'title',
                 'description',
                 'picture_filename',
                 'picture_link',
                 'has_money',
                 'phrase_count']
