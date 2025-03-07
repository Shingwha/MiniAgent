from MiniAgent.tools import BochaSearch




if __name__ == '__main__':
    tool = BochaSearch(api_key='')
    results = tool.execute(query='车企在二月份的销量')
    print(results)