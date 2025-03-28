from duckduckgo_search import DDGS
from MiniAgent.core.tool import tool
import requests
from readability import Document
from bs4 import BeautifulSoup


@tool(description="搜索引擎，可获取新闻的标题和摘要以及链接")
def duckduckgo_search(query):
    max_results = 3
    with DDGS() as ddgs:
        results = []
        # 进行搜索并获取结果
        for r in ddgs.text(query, max_results=max_results):
            results.append(r)
        return results


@tool(description="在使用duckduckgo_search获取新闻链接后，使用此方法获取新闻的完整内容")
def fetch_web_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://www.google.com/",
    }
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 自动检测编码
        response.encoding = response.apparent_encoding

        # 使用readability提取核心内容
        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), "html.parser")

        # 清理格式并获取纯文本
        content = soup.get_text(separator="\n", strip=True)

        return {"title": doc.title(), "content": content}

    except Exception as e:
        print(f"抓取失败：{str(e)}")
        return None
