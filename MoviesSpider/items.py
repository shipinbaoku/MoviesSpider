# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Identity
from scrapy.loader import ItemLoader
from scrapy.loader.common import wrap_loader_context
from scrapy.utils.misc import arg_to_iter

from models.film import VodDetail, PlayUrl
from utils.common import date_convert


def MergeDict(dict1, dict2):
    return dict2.update(dict1)
    pass


class MapComposeCustom(MapCompose):
    # 自定义MapCompose，当value没元素时传入" "
    def __call__(self, value, loader_context=None):
        if not value:
            value.append(" ")
        values = arg_to_iter(value)
        if loader_context:
            context = MergeDict(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
        for func in wrapped_funcs:
            next_values = []
            for v in values:
                next_values += arg_to_iter(func(v))
            values = next_values
        return values


class TakeFirstCustom(TakeFirst):
    """
    处理采集的元素不存在问题
    """

    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value.strip() if isinstance(value, str) else value


"""
重写ItemLoader,默认取第一个元素并处理不存在的元素
"""


class MoviesItemLoader(ItemLoader):
    default_output_processor = TakeFirstCustom()
    default_input_processor = MapComposeCustom()


class MoviesspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class OkzyMoviesDetailspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    url_id = scrapy.Field()
    vod_title = scrapy.Field()
    vod_sub_title = scrapy.Field()
    vod_blurb = scrapy.Field()
    vod_content = scrapy.Field()
    vod_status = scrapy.Field()
    vod_type = scrapy.Field()
    vod_class = scrapy.Field()
    vod_tag = scrapy.Field()
    vod_pic_url = scrapy.Field(
        output_processor=Identity())  # 优先级高于default_output_processor，因为scrapy要求下载图片、文件，不能是字符串，所以默认处理
    vod_pic_path = scrapy.Field()  # 下载的图片保存路径
    vod_pic_thumb = scrapy.Field()
    vod_actor = scrapy.Field()
    vod_director = scrapy.Field()
    vod_writer = scrapy.Field()
    vod_remarks = scrapy.Field()
    vod_pubdate = scrapy.Field()
    vod_area = scrapy.Field()
    vod_lang = scrapy.Field()
    vod_year = scrapy.Field()
    vod_hits = scrapy.Field()
    vod_hits_day = scrapy.Field()
    vod_hits_week = scrapy.Field()
    vod_hits_month = scrapy.Field()
    vod_up = scrapy.Field()
    vod_down = scrapy.Field()
    vod_score = scrapy.Field()
    vod_score_all = scrapy.Field()
    vod_score_num = scrapy.Field()
    vod_create_time = scrapy.Field(input_processor=MapCompose(date_convert))
    vod_update_time = scrapy.Field(input_processor=MapCompose(date_convert))
    vod_lately_hit_time = scrapy.Field()
    pass

    def save_into_sql(self):
        if not VodDetail.table_exists():
            VodDetail.create_table()
        vod_detail = VodDetail.get_or_none(VodDetail.url_id == self['url_id'])
        if vod_detail is not None:
            data = vod_detail
        else:
            data = VodDetail()
        try:
            data.url = self['url']
            data.url_id = self['url_id']
            data.vod_title = self['vod_title']
            data.vod_sub_title = self['vod_sub_title']
            # data.vod_blurb = self['vod_blurb']
            data.vod_content = self['vod_content']
            data.vod_status = 1
            data.vod_type = self['vod_type']
            data.vod_class = self['vod_class']
            # data.vod_tag=self['vod_tag']
            data.vod_pic_url = self['vod_pic_url'][0]
            data.vod_pic_path = self['vod_pic_path']
            # data.vod_pic_thumb=self['vod_pic_thumb']
            data.vod_actor = self['vod_actor']
            data.vod_director = self['vod_director']
            # data.vod_writer=self['vod_writer']
            data.vod_remarks = self['vod_remarks']
            # data.vod_pubdate=self['vod_pubdate']
            data.vod_area = self['vod_area']
            data.vod_lang = self['vod_lang']
            data.vod_year = self['vod_year']
            # data.vod_hits=self['vod_hits']
            # data.vod_hits_day=self['vod_hits_day']
            # data.vod_hits_week=self['vod_hits_week']
            # data.vod_hits_month=self['vod_hits_month']
            # data.vod_up=self['vod_up']
            # data.vod_down=self['vod_down']
            data.vod_score = self['vod_score']
            data.vod_score_all = self['vod_score_all']
            data.vod_score_num = self['vod_score_num']
            data.vod_create_time = self['vod_create_time']
            data.vod_update_time = self['vod_update_time']
            # data.vod_lately_hit_time = self['vod_lately_hit_time']
            row = data.save()

        except Exception as e:
            print(e)
            pass


class OkzyMoviesspiderPlayurlItem(scrapy.Item):
    play_title = scrapy.Field()
    play_from = scrapy.Field()
    play_url = scrapy.Field()
    play_url_aes = scrapy.Field()
    url_id = scrapy.Field()
    create_time = scrapy.Field(input_processor=MapCompose(date_convert))
    update_time = scrapy.Field(input_processor=MapCompose(date_convert))

    def save_into_sql(self):
        if not PlayUrl.table_exists():
            PlayUrl.create_table()
        play_url = PlayUrl.get_or_none(PlayUrl.play_url_aes == self['play_url_aes'])
        if play_url is not None:
            data = play_url
        else:
            data = PlayUrl()
        try:
            data.play_title = self['play_title']
            data.play_from = self['play_from']
            data.play_url = self['play_url']
            data.play_url_aes = self['play_url_aes']
            data.url_id = self['url_id']
            data.create_time = self['create_time']
            data.update_time = self['update_time']
            row = data.save()
        except Exception as e:
            print(e)
        pass

    pass
