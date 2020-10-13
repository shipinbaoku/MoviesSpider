# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy import Request
# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline

from utils.common import pinyin


class MoviesspiderPipeline:
    def process_item(self, item, spider):
        return item


# 重写scrapy.pipelines.images.ImagesPipeline 获取图片下载地址 给items

class MovieImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if "vod_pic_url" in item:
            for vod_pic_url in item['vod_pic_url']:
                yield Request(url=vod_pic_url, meta={'item': item})  # 添加meta是为了下面重命名文件名使用

    def file_path(self, request, response=None, info=None):

        item = request.meta['item']
        movietitle = item['vod_title']
        #去除特殊字符，只保留汉子，字母、数字
        sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", movietitle)
        img_guid = request.url.split('/')[-1]  # 得到图片名和后缀
        filename = '/upload/images/{0}/{1}'.format(pinyin(sub_str), img_guid)
        return filename

        # return super().file_path(request, response, info)

    # def thumb_path(self, request, thumb_id, response=None, info=None):
    #     item = request.meta['item']
    #     movietitle = pinyin(item['vod_title'][0])
    #     img_guid = request.url.split('/')[-1]  # 得到图片名和后缀
    #     filename = '/images/{0}/thumbs/{1}/{2}'.format(movietitle, thumb_id, img_guid)
    #     return filename

    def item_completed(self, results, item, info):
        image_file_path = ""
        if "vod_pic_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["vod_pic_path"] = image_file_path
        return item


class MysqlPipeline(object):

    def process_item(self, item, spider):
        """
        每个item中都实现save_into_sql()方法，就可以用同一个MysqlPipeline去处理
        :param item:
        :param spider:
        :return:
        """
        item.save_into_sql()
        return item
