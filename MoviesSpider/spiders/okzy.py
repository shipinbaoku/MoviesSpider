from urllib import parse

import scrapy
from scrapy import Request

from MoviesSpider.items import OkzyMoviesDetailspiderItem, OkzyMoviesspiderPlayurlItem, MoviesItemLoader
from utils import common


class OkzySpider(scrapy.Spider):
    name = 'okzy'
    allowed_domains = ['okzy.co']
    start_urls = ['https://okzy.co/?m=vod-index-pg-1.html']
    # start_urls = ['https://okzy.co/?m=vod-type-id-22-pg-1.html']

    def parse(self, response):
        all_urls = response.css(".xing_vb4 a::attr(href)").extract()
        for url in all_urls:
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail)

        list_urls = list(range(1, 6))
        list_urls.reverse()
        for i in list_urls:
            url = 'https://okzy.co/?m=vod-index-pg-{0}.html'.format(i)
            yield Request(url=url, dont_filter=True, callback=self.parse)

    def parse_detail(self, response):
        voddetail_item_loader = MoviesItemLoader(item=OkzyMoviesDetailspiderItem(), response=response)
        voddetail_item_loader.add_value('url', response.url)
        voddetail_item_loader.add_value("url_id", common.get_md5(response.url))
        voddetail_item_loader.add_css('vod_title', 'h2::text')
        voddetail_item_loader.add_css('vod_sub_title',
                                      '.vodinfobox > ul:nth-child(1) > li:nth-child(1) > span:nth-child(1)::text')
        # voddetail_item_loader.add_xpath('vod_blurb', '//h2/text()')
        voddetail_item_loader.add_css('vod_content', 'div.ibox:nth-child(2) > div:nth-child(2)::text')
        # voddetail_item_loader.add_xpath('vod_status', '//h2/text()')
        voddetail_item_loader.add_css('vod_type',
                                      '.vodinfobox > ul:nth-child(1) > li:nth-child(4) > span:nth-child(1)::text')
        voddetail_item_loader.add_xpath('vod_class',
                                        '/html/body/div[5]/div[1]/div/div/div[2]/div[2]/ul/li[4]/span/a/text()')
        # voddetail_item_loader.add_xpath('tag', '//h2/text()'
        voddetail_item_loader.add_css('vod_pic_url', '.lazy::attr(src)')
        # voddetail_item_loader.add_xpath('vod_pic_thumb', '//h2/text()')
        voddetail_item_loader.add_css('vod_actor',
                                      '.vodinfobox > ul:nth-child(1) > li:nth-child(3) > span:nth-child(1)::text')
        voddetail_item_loader.add_css('vod_director',
                                      '.vodinfobox > ul:nth-child(1) > li:nth-child(2) > span:nth-child(1)::text')
        # voddetail_item_loader.add_xpath('vod_writer', '//h2/text()')
        voddetail_item_loader.add_css('vod_remarks', '.vodh > span:nth-child(2)::text')
        # voddetail_item_loader.add_xpath('vod_pubdate', '//h2/text()')
        voddetail_item_loader.add_css('vod_area', 'li.sm:nth-child(5) > span:nth-child(1)::text')
        voddetail_item_loader.add_css('vod_lang', 'li.sm:nth-child(6) > span:nth-child(1)::text')
        voddetail_item_loader.add_css('vod_year', 'li.sm:nth-child(7) > span:nth-child(1)::text')
        # voddetail_item_loader.add_xpath('vod_hits', '//h2/text()')
        # voddetail_item_loader.add_xpath('vod_hits_day', '//h2/text()')
        # voddetail_item_loader.add_xpath('vod_hits_week', '//h2/text()')
        # voddetail_item_loader.add_xpath('vod_hits_month', '//h2/text()')
        # voddetail_item_loader.add_xpath('vod_up', '//h2/text()')
        # voddetail_item_loader.add_xpath('vod_down', '//h2/text()')
        voddetail_item_loader.add_css('vod_score', '.vodh > label:nth-child(3)::text')
        voddetail_item_loader.add_css('vod_score_all', 'li.sm:nth-child(12) > span:nth-child(1)::text')
        voddetail_item_loader.add_css('vod_score_num', 'li.sm:nth-child(13) > span:nth-child(1)::text')
        voddetail_item_loader.add_css('vod_create_time', 'li.sm:nth-child(9) > span:nth-child(1)::text')
        voddetail_item_loader.add_css('vod_update_time', 'li.sm:nth-child(9) > span:nth-child(1)::text')
        # voddetail_item_loader.add_xpath('vod_lately_hit_time', '//h2/text()')
        okzyMoviesspiderItem = voddetail_item_loader.load_item()

        # 解析m3u8格式播放地址
        ckm3u8playurlList = response.xpath('//*[@id="2"]/ul/li/text()').extract()
        for ckm3u8playurlInfo in ckm3u8playurlList:
            m3u8playurlInfoList = ckm3u8playurlInfo.split('$')
            vodm3u8playurl_item_loader = MoviesItemLoader(item=OkzyMoviesspiderPlayurlItem(), response=response)
            vodm3u8playurl_item_loader.add_value('play_title', m3u8playurlInfoList[0])
            vodm3u8playurl_item_loader.add_value('play_url', m3u8playurlInfoList[1])
            vodm3u8playurl_item_loader.add_value('play_url_aes', common.get_md5(m3u8playurlInfoList[1]))
            vodm3u8playurl_item_loader.add_xpath('play_from', '//*[@id="2"]/h3/span/text()')
            vodm3u8playurl_item_loader.add_value("url_id", common.get_md5(response.url))
            vodm3u8playurl_item_loader.add_css('create_time', 'li.sm:nth-child(9) > span:nth-child(1)::text')
            vodm3u8playurl_item_loader.add_css('update_time', 'li.sm:nth-child(9) > span:nth-child(1)::text')
            okzyMoviesm3u8PlayurlspiderItem = vodm3u8playurl_item_loader.load_item()
            yield okzyMoviesm3u8PlayurlspiderItem
        # 解析mp4格式播放地址
        mp4playurlList = response.xpath('//*[@id="down_1"]/ul/li/text()').extract()
        for mp4playurlInfo in mp4playurlList:
            mp4playurlInfoList = mp4playurlInfo.split('$')
            vodmp4playurl_item_loader = MoviesItemLoader(item=OkzyMoviesspiderPlayurlItem(), response=response)
            vodmp4playurl_item_loader.add_value('play_title', mp4playurlInfoList[0])
            vodmp4playurl_item_loader.add_value('play_url', mp4playurlInfoList[1])
            vodmp4playurl_item_loader.add_value('play_url_aes', common.get_md5(mp4playurlInfoList[1]))
            vodmp4playurl_item_loader.add_xpath('play_from', '//*[@id="down_1"]/h3/span/text()')
            vodmp4playurl_item_loader.add_value("url_id", common.get_md5(response.url))
            vodmp4playurl_item_loader.add_css('create_time', 'li.sm:nth-child(9) > span:nth-child(1)::text')
            vodmp4playurl_item_loader.add_css('update_time', 'li.sm:nth-child(9) > span:nth-child(1)::text')
            okzyMoviesmp4PlayurlspiderItem = vodmp4playurl_item_loader.load_item()
            yield okzyMoviesmp4PlayurlspiderItem
        yield okzyMoviesspiderItem
