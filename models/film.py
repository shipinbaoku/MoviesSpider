from peewee import *

# database = MySQLDatabase('film', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': 'root'})
from models.retry_mySQLDatabase import RetryMySQLDatabase

database = database = RetryMySQLDatabase.get_db_instance()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class PlayUrl(BaseModel):
    create_time = IntegerField(null=True)
    play_from = CharField(null=True)
    play_title = CharField(null=True)
    play_url = CharField()
    play_url_aes = CharField()
    update_time = IntegerField(null=True)
    url_id = CharField(unique=True)

    class Meta:
        table_name = 'play_url'


class VodDetail(BaseModel):
    url = CharField()
    url_id = CharField(unique=True)
    vod_actor = CharField(null=True)
    vod_area = CharField(null=True)
    vod_blurb = CharField(null=True)
    vod_class = CharField(null=True)
    vod_content = TextField(null=True)
    vod_create_time = IntegerField(null=True)
    vod_director = CharField(null=True)
    vod_down = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_hits = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_hits_day = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_hits_month = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_hits_week = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_lang = CharField(null=True)
    vod_lately_hit_time = IntegerField(null=True)
    vod_pic_path = CharField(null=True)
    vod_pic_thumb = CharField(null=True)
    vod_pic_url = CharField(null=True)
    vod_pubdate = IntegerField(null=True)
    vod_remarks = CharField(null=True)
    vod_score = DecimalField(constraints=[SQL("DEFAULT 0.0")], null=True)
    vod_score_all = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_score_num = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_sub_title = CharField(null=True)
    vod_tag = CharField(null=True)
    vod_title = CharField()
    vod_type = CharField(null=True)
    vod_up = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vod_update_time = IntegerField(null=True)
    vod_writer = CharField(null=True)
    vod_year = CharField(null=True)

    class Meta:
        table_name = 'vod_detail'


class VodTags(BaseModel):
    frequency = IntegerField(null=True)
    name = CharField()

    class Meta:
        table_name = 'vod_tags'


class VodType(BaseModel):
    type_des = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_en = CharField(constraints=[SQL("DEFAULT ''")], index=True, null=True)
    type_extend = TextField(null=True)
    type_jumpurl = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_key = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_logo = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_mid = IntegerField(constraints=[SQL("DEFAULT 1")], index=True, null=True)
    type_name = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    type_pic = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_pid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    type_sort = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    type_status = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    type_title = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_tpl = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_tpl_detail = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_tpl_down = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_tpl_list = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_tpl_play = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type_union = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = 'vod_type'
