# coding:utf-8

import pandas as pd


class RequestObj:

    def my_requests(self):
        pass

    def parse_data(self, data):
        pass

    def save(self, data: list):
        """功能：保存data数据到sql表day_rank中s
        data参数定义如下
        data:{
        platform:'1' ,  # 1：汽车之家 2：懂车帝  3：易车  4：其他
        daily_heat: int , # 每日热度值
        add_time: datetime , # 默认当前时间
        car_name: str , # 汽车名称
        rank: int, # 排名
        jibie: str, #  汽车级别，小型SUV 紧凑型SUV 紧凑型车。。
        }
        """

        # if 'platform' in data and 'daily_heat' in data and \
        #         'car_name' in data and 'rank' in data and 'jibie' in data:
        try:
            # 保存数据
            # data_list = []
            df = pd.DataFrame(data)
            df.to_csv('dongchediRank.csv')

        except Exception as e:
            raise ValueError(f'数据保存错误：{e}')
        # else:
        #     raise ValueError('data参数错误')

    def task_run(self):
        self.my_requests()

# if __name__ == '__main__':
#     client = RequestObj()
#     client.save({
#         "platform": "1",
#         "daily_heat": 134,
#         "car_name": "test02",
#         "add_time": datetime.datetime.now(),
#         "rank": 1
#     })
