from pathlib import Path

BOT_NAME = "parser_fixprice"

SPIDER_MODULES = ["parser_fixprice.spiders"]
NEWSPIDER_MODULE = "parser_fixprice.spiders"

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   "parser_fixprice.pipelines.ParserFixpricePipeline": 300,
}

PATH = Path(__file__).parent.parent.resolve()
DOWNLOAD_DIR = PATH / "data"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# DOCKER
FLARE_SOLVER_URL = 'http://flaresolver:8191/v1'
# LOCAL
# FLARE_SOLVER_URL = 'http://localhost:8191/v1'

URL = 'https://fix-price.com'
URL_CATALOG = 'https://fix-price.com/catalog'
# city 'Екатеринбург'
LOCALITY = ('%7B%22city%22%3A%22%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0'
            '%BD%D0%B1%D1%83%D1%80%D0%B3%22%2C%22cityId%22%3A55%2C'
            '%22longitude%22%3A60.597474%2C%22latitude%22%3A56.838011%2C'
            '%22prefix%22%3A%22%D0%B3%22%7D')
# Указываем категории для парсинга, если пустой список парсит весь сайт
CATEGORY_PARSE_URL = []
