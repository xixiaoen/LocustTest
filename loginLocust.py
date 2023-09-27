from locust import HttpUser
from locust import task
import os
from generate import ApplicationJsonRequest


# 我们在做接口自动化测试时，使用的是request对接口发起请求，在这里我们用的是locust中的httpuser对接口进行发起请求
class Opms(HttpUser):
    def on_start(self):
        print("我是一个用户，我启动了")

    def on_stop(self):
        print("我是一个用户，我退出了")

    # 定义好的接口必须使用task装饰器使其成为一个需要执行的任务，否则的话即使启动了locust也不会将定义好的函数作为一个需要执行的任务
    @task
    def main(self):
        url = "http://openai.100tal.com/aitext/ch-composition/text-correction"

        url_params = dict()
        # 根据接口要求，填写真实URL参数。key1、key2仅做举例
        body_params = {
            "user_id": "xxxx-xxxx-xxxx-xxxx",
            "user_name": "小明",
            "grade": 1,
            "min_text_length": 200,
            "max_text_length": 1200,
            "topic_type": 1,
            "answer_title": "放风筝",
            # "answer_text": ['“草长莺飞二月天，拂堤杨柳醉春烟。”生机勃勃的春天来到了，这正是放风筝的好时节。 ', '郊外小朋友们正兴致勃勃地放着风筝'],
            "answer_url": ["https://igpicture.boe.com/ai_exercise/test/2851695021315_.pic.jpg"],
            "answer_base64": [""],
            "correction_type": 0,
            "max_score": 100,
            "requirement": 1,
            "knowledge": 1,
            "is_fragment": 1,
            "comment_type": 1,
            "spell_type": 0,
            "rotate_model": 1
        }

        access_key_id = "1143550461945577472"
        access_key_secret = "e9be97b8c4dc46c78f91f7fb8773eba0"

        # 生成签名
        a = ApplicationJsonRequest(url=url, access_key_id=access_key_id, access_key_secret=access_key_secret,
                               body_params=body_params, url_params=url_params)
        a.get_signature()

        # 生成URL
        url = url + '?' + a.url_format(a.url_params)
        print(url)

        with self.client.post(url, json=a.body_params, headers=a.headers, name="登录", catch_response=True) as res:
            print(res.json())
            if res.json()["code"] == 20000:
                res.success()
            else:
                res.failure("fail")


if __name__ == '__main__':
    os.system("locust -f loginLocust.py --web-host=127.0.0.1")