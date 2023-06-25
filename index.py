# coding:utf-8

import io
import datetime
import traceback
import zipfile
import csv
import time

import requests
from request_tool import RequestObj
from baidu_client import BaiduClient


class BaiduZhiShu(RequestObj):
    def __init__(self, *args, **kwargs):
        self.b_username = 'demo'  # 你的百度账号名称
        self.b_token = "你的百度token"  # 百度账号token
        self.keywords = ['长安马自达', "马自达cx-30"]  # 需要查询的关键字列表

    def parse_data(self, url, query_type='search'):
        try:
            res = requests.get(url)
            zip_file = zipfile.ZipFile(io.BytesIO(res.content))

            # 解压缩zip文件
            # 遍历zip文件内的文件列表
            for filename in zip_file.namelist():
                if filename.endswith('.csv'):
                    # 找到csv文件并读取
                    with zip_file.open(filename) as f:
                        reader = csv.reader(io.TextIOWrapper(f, encoding='gbk'))
                        data = [row for row in reader]
                        break  # 找到csv文件后退出循环

            if query_type == "search":
                title_data = data[0][3:]
                detail_data = data[1:]
            else:
                title_data = data[0][2:]
                detail_data = data[1:]

            final_data = []
            for detail_list in detail_data:
                title_data_list = detail_list[3:] if query_type == 'search' else detail_list[2:]

                temp_keyword = detail_list[0]
                count_item = 0
                for item in title_data_list:
                    temp_add_time = datetime.datetime.strptime(title_data[count_item], '%Y%m%d')
                    temp_heat_value = str(item)

                    final_data.append({
                        "keyword": temp_keyword,
                        "add_time": temp_add_time,
                        "heat_value": int(temp_heat_value) if temp_heat_value.isdigit() else 0,
                        "query_type": 1 if query_type == 'search' else 2
                    })
                    count_item += 1

            return final_data
        except Exception as e:
            print(f'百度搜索指数数据解析错误：{e}: {traceback.format_exc()}')
            return []

    def get_search_index(self, keywords: list, start_time: str, end_time: str):
        """获取搜索指数数据"""
        query_type = 'search'
        # 获取excle下载链接
        client = BaiduClient(b_token=self.b_token, b_username=self.b_username)
        task_data = client.create_task(
            keywords=keywords,
            start_time=start_time,
            end_time=end_time,
            query_type=query_type
        )

        download_url = None
        if task_data.get('status', None):
            while True:
                time.sleep(1)
                download_url = client.get_result(task_data.get('task'))
                if download_url == "not_finished":
                    time.sleep(2)
                else:
                    break
        # 下载解析链接内容， 返回数据
        if download_url is not None:
            data_list = self.parse_data(download_url, query_type=query_type)
            # 保存数据
            self.save(data_list)

        else:
            print('报错：百度指数download_url获取失败')
            raise ValueError('报错：百度指数download_url获取失败')

    def get_feed_index(self, keywords: list, start_time: str, end_time: str):
        """获取资讯指数数据"""
        # 获取excle下载链接
        query_type = 'feed'
        client = BaiduClient(b_token=self.b_token, b_username=self.b_username)
        task_data = client.create_task(
            keywords=keywords,
            start_time=start_time,
            end_time=end_time,
            query_type=query_type
        )

        download_url = None
        if task_data.get('status', None):
            while True:
                time.sleep(1)
                download_url = client.get_result(task_data.get('task'))
                if download_url == "not_finished":
                    time.sleep(2)
                else:
                    break
        # 下载解析链接内容， 返回数据
        if download_url is not None:
            data_list = self.parse_data(download_url, query_type=query_type)
            # 保存数据
            self.save(data_list)

        else:
            print('报错：百度资讯download_url获取失败')
            raise ValueError('报错：百度资讯download_url获取失败')

    def my_requests(self):
        try:
            # 需要搜索的keywords
            keywords = self.keywords

            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=2)  # 计算昨天的日期
            yesterday_str = yesterday.strftime('%Y-%m-%d')  # # 将昨天的日期转换为字符串

            # 搜索指数
            self.get_search_index(keywords=keywords, start_time=yesterday_str, end_time=yesterday_str)
            # 资讯指数
            self.get_feed_index(keywords=keywords, start_time=yesterday_str, end_time=yesterday_str)
            print(f'百度指数数据({yesterday_str})获取完成, {datetime.datetime.now()}')

        except Exception as e:
            print(f"百度指数 报错=={e}=={traceback.format_exc()}")


if __name__ == '__main__':
    dongchedi = BaiduZhiShu()
    dongchedi.task_run()
