import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'cnblogs'])
# execute(['scrapy', 'crawl', 'zhihuCookiesPool'])
# execute(['scrapy', 'crawl', 'zhihu'])
execute(['scrapy', 'crawl', 'okzy'])