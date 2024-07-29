import re
from datetime import datetime

import scrapy

from .. import utils
from .. import xpathes
from ..items import ParserFixpriceItem
from ..settings import FLARE_SOLVER_URL, LOCALITY, URL, URL_CATALOG

categories_tree = []
list_products = []
cookies = {}
user_agent = ''


class FixpriceSpider(scrapy.Spider):
    name = 'fixprice'
    handle_httpstatus_list = [404]
    page_num = 1
    start_url_page = ''

    def start_requests(self):
        yield scrapy.Request(
            url=FLARE_SOLVER_URL,
            body=utils.get_fs_body(URL),
            headers={"Content-Type": "application/json"},
            callback=self.main_page,
            method="POST",
        )

    def main_page(self, response):
        response, cooks, usr_agent = utils.parse_fs_response(response)
        cooks['locality'] = LOCALITY
        cookies = cooks
        user_agent = usr_agent

        yield scrapy.Request(
            url=URL_CATALOG,
            cookies=cookies,
            headers={"User-Agent": user_agent},
            callback=self.parse_category_tree,
            method="GET",
        )

    def parse_category_tree(self, response):
        sections = response.xpath(xpathes.category_tree)

        for sec in sections:
            sec_name = sec.xpath(xpathes.cat_name).get()
            sec_href = sec.xpath(xpathes.cat_href).get()

            if sec.xpath(xpathes.sub_class):
                sub_sections = sec.xpath(xpathes.sub_class)

                for sub_sec in sub_sections:
                    sub_name = sub_sec.xpath(xpathes.subcat_name).get()
                    sub_href = sub_sec.xpath(xpathes.subcat_href).get()
                    categories_tree.append(
                        {'section': [sec_name, sub_name], 'url': URL + sub_href}
                    )
            else:
                categories_tree.append(
                    {'section': [sec_name], 'url': URL + sec_href}
                )

        # Указываем категории для парсинга либо убираем срез и парсим всё
        for category in categories_tree[1:10]:
            yield scrapy.Request(
                url=category['url'],
                cookies=cookies,
                headers={"User-Agent": user_agent},
                callback=self.parse_list_products,
                method="GET",
                meta={'section': category['section']},
            )

    def parse_list_products(self, response):
        if response.status == 404 or not response.xpath(xpathes.products_names):
            for product in list_products:
                yield scrapy.Request(
                    url=product['url'],
                    cookies=cookies,
                    headers={"User-Agent": user_agent},
                    callback=self.parse_product,
                    method="GET",
                    meta={'section': response.meta['section']},

                )
        else:
            products_names = response.xpath(xpathes.products_names).getall()
            products_links = response.xpath(xpathes.products_links).getall()

            for name, link in zip(products_names, products_links):
                list_products.append({'name': name, 'url': URL + link, })

            if self.page_num == 1:
                self.start_url_page = response.url
            self.page_num += 1

            next_page = self.start_url_page + f'?page={self.page_num}'
            yield scrapy.Request(
                url=next_page,
                cookies=cookies,
                headers={"User-Agent": user_agent},
                callback=self.parse_list_products,
                method="GET",
                meta={'section': response.meta['section']},
            )

    def parse_product(self, response):
        timestamp = int(datetime.now().timestamp())
        url = response.url
        title = response.xpath(xpathes.title).get()
        description = response.xpath(xpathes.description).get()
        main_image = response.xpath(xpathes.images).get()
        set_images = response.xpath(xpathes.images).getall()
        sections = response.meta['section']

        properties = {}
        for prop in response.xpath(xpathes.properties):
            prop_name = prop.xpath(xpathes.prop_name).get()

            if prop_name == 'Бренд':
                prop_value = prop.xpath(xpathes.brand).get()
            else:
                prop_value = prop.xpath(xpathes.prop_value).get()

            properties[prop_name] = prop_value

        if response.xpath(xpathes.extra_prop):
            for prop in response.xpath(xpathes.extra_prop):
                prop_name = prop.xpath(xpathes.prop_name).get()
                prop_value = prop.xpath(xpathes.prop_value).get()
                properties[prop_name] = prop_value

        rpc = properties['Код товара'] if 'Код товара' in properties else None
        brand = properties['Бренд'] if 'Бренд' in properties else 'Не указан'

        script = response.xpath(xpathes.script).get()
        product_script = re.search(r'\.product=(\{.*?\})', script).group(1)
        pattern = r'specialPrice:{price:"(.*?)",'
        current = (
            float(re.search(pattern, product_script).group(1))
            if re.search(pattern, product_script)
            else None
        )
        original = float(response.xpath(xpathes.original_price).get())
        sale_tag = ""

        if current:
            discount_percentage = round(100 - ((current / original) * 100))
            sale_tag = f"Скидка {discount_percentage}%"
        else:
            current = original

        marketing_tags = (
            [response.xpath(xpathes.tags).get()]
            if response.xpath(xpathes.tags) else []
        )

        yield ParserFixpriceItem(
            timestamp=timestamp,
            RPC=rpc,
            url=url,
            title=title,
            marketing_tags=marketing_tags,
            brand=brand,
            section=sections,
            price_data=dict(
                current=current,
                original=original,
                sale_tag=sale_tag,
            ),
            stock=dict(
                in_stock=True,
                count=0
            ),
            assets=dict(
                main_image=main_image,
                set_images=set_images,
                view360=[],
                video=[],
            ),
            metadata={
                "__description": description,
                **properties
            },
            variants=1
        )
