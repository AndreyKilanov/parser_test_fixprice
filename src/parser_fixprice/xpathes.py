# category and subcategories
category_tree = '//div[@class="category-tree"]/div[@class="accordion"]'
cat_name = './/button[@class="button"]//a/text()'
cat_href = './/button[@class="button"]//a/@href'
sub_class = './/div[@class="panel"]//a[@class="title subtitle"]'
subcat_name = './text()'
subcat_href = './@href'
# lincs product
products_names = '//div[@class="products"]//div[@class="description"]/a/text()'
products_links = '//div[@class="products"]//div[@class="description"]/a/@href'
# product
title = '//div[@class="product-details"]//h1/text()'
description = '//div[@class="product-details"]//div[@class="description"]/text()'
images = '//div[@class="slider gallery"]//img[@class="normal"]/@src'
# properties
properties = '//div[@class="properties"]/p[@class="property"]'
prop_name = './/span[@class="title"]/text()'
prop_value = './/span[@class="value"]/text()'
brand = '//span[@class="value"]//a/text()'
extra_prop = '//div[@class="properties extra-properties"]/p[@class="property"]'
# price
original_price = '//meta[@itemprop="price"]/@content'
script = '//script[contains(text(), "window.__NUXT__")]/text()'
# sale tag
tags = '//div[@class="auth-block"]//p/text()'
