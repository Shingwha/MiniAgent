from MiniAgent.core.tool import Tool

import requests
import json
from datetime import datetime

class BochaSearch(Tool):
    def __init__(self,api_key):
        self.api_key = api_key
        super().__init__(name="bocha_search", description="当你不知道某些信息的时候，通过这个bocha搜索新闻或其他信息", func=self.bocha_search)

    def bocha_search(self,query):
        url = "https://api.bochaai.com/v1/web-search"
        payload = json.dumps({
            "query": query,
            "freshness": "noLimit",
            "summary": True,
            "count": 10,
        })
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        raw_data = response.json()

        if raw_data.get("code") == 200:
            filtered_results = []
            formatted_results = []
            # 直接访问 webPages.value 数组
            for item in raw_data.get("data", {}).get("webPages", {}).get("value", []):
                # 处理日期格式
                date_str = item.get("dateLastCrawled")
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                except (ValueError, TypeError):
                    date = None

                filtered = {
                    "name": item.get("name"),
                    "url": item.get("url"),
                    "snippet": item.get("snippet"),
                    "summary": item.get("summary"),
                    "dateLastCrawled": date
                }
                filtered_results.append(filtered)

            # 按日期倒序排列
            filtered_results.sort(key=lambda x: x["dateLastCrawled"], reverse=True)

            # 格式化每条新闻信息
            for idx, item in enumerate(filtered_results, start=1):
                formatted = (
                    f"新闻 {idx}:\n"
                    f"标题: {item['name']}\n"
                    f"链接: {item['url']}\n"
                    f"摘要: {item['snippet']}\n"
                    f"总结: {item['summary']}\n"
                    f"时间: {item['dateLastCrawled'].strftime('%Y-%m-%d %H:%M:%S') if item['dateLastCrawled'] else '未知'}"
                )
                formatted_results.append(formatted)

            return formatted_results
        else:
            return raw_data

if __name__ == '__main__':
    tool = BochaSearch(api_key='')
    result = tool.execute(query='AI科技新闻')
    print(results)