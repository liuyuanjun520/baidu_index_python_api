# coding:utf-8

import json
import requests
import traceback


class BaiduClient(object):
    def __init__(self, b_token: str, b_username: str):
        self.username = b_username  # 百度账号名称
        self.baidu_token = b_token  # 百度账号token

    def get_token(self):
        """获取token"""
        try:
            # 后续可以新增其他操作，比如从redis中获取token
            return self.baidu_token
        except Exception as e:
            print(f'百度指数从redis获取token错误，{e}：{traceback.format_exc()}')
            raise ValueError("redis get token error")

    def create_task(self, keywords: list, start_time: str, end_time: str, query_type: str):
        """创建任务
        """
        try:
            username = self.username
            token = self.get_token()
            url = "https://api.baidu.com/json/sms/service/IndexApiService/createTask"
            query_type = 'search' if query_type == 'search' else "feed"
            user_payload = {
                "header": {
                    "accessToken": token,
                    "userName": username,
                    "action": "API-PYTHON"
                },
                "body": {
                    "datasource": query_type,
                    "dateRange": {
                        "start": start_time,
                        "end": end_time
                    },
                    "device": [
                        "all"
                    ],
                    "region": {
                        "province": [],
                        "city": [],
                        "isAll": True
                    },
                    "keyword": keywords
                }
            }
            http_headers = {
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            user_payload = json.dumps(user_payload)
            response = requests.request("POST", url, data=user_payload, headers=http_headers)
            data = json.loads(response.content)
            if data.get("header", {}).get("status", None) == 0:
                body = data.get("body", {}).get("data", [])
                return {
                    "status": True,
                    "task": body[0].get("taskId")
                }
            elif data.get("header", {}).get("status", None) == 2:
                print('百度错误')
            else:
                print('百度创建任务接口返回错误')
                return {
                    "status": False,
                    "task": None
                }
        except Exception as e:
            print(f'百度指数createTask接口错误，{e}：{traceback.format_exc()}')
            return {
                "status": False,
                "task": None
            }

    def get_result(self, task_id):
        """查询任务状态"""
        try:
            url = "https://api.baidu.com/json/sms/service/IndexApiService/getResult"
            user_payload = {
                "header": {
                    "userName": self.username,
                    "accessToken": self.get_token(),
                    "action": "API-PYTHON"
                },
                "body": {
                    "taskId": task_id
                }
            }
            http_headers = {
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            user_payload = json.dumps(user_payload)
            response = requests.request("POST", url, data=user_payload, headers=http_headers)
            data = json.loads(response.content)
            if data.get("header", {}).get("status", None) == 0:
                body = data.get("body", {}).get("data", [])
                if body[0].get("status", None) == "finished":
                    return body[0].get("resultUrl")
                else:
                    return "not_finished"
            else:
                print(f'百度指数getResult接口返回错误')
                return None
        except Exception as e:
            print(f'百度指数getResult接口错误，{e}：{traceback.format_exc()}')
            return None

    def refresh_token(self):
        """刷新token
        百度token的过期时间是24h，超过24h的token无法使用，且只能通过手动从百度账号面板中刷新重新获取
        """
        try:
            url = "https://api.baidu.com/json/sms/service/IndexApiService/refreshAccessToken"
            user_payload = {
                "header": {
                    "userName": self.username,
                    "accessToken": self.get_token(),
                    "action": "API-PYTHON"
                },
                "body": {}
            }
            http_headers = {
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            user_payload = json.dumps(user_payload)
            response = requests.request("POST", url, data=user_payload, headers=http_headers)
            data = json.loads(response.content)
            if data.get("header", {}).get("status", None) == 0:
                body = data.get("body", {}).get("data", [])
                self.baidu_token = body[0].get("accessToken")
                print('百度token刷新成功')
            else:
                print('报错：百度token刷新失败')
        except Exception as e:
            print(f'百度token刷新出错：{e}： {traceback.format_exc()}')

    # 查询关键字是否收录
    def check_keywords(self, data):
        return None


if __name__ == '__main__':
    pass
