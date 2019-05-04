# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'pdd_proxies'

# 测试URL，建议抓哪个网站测哪个
TEST_URL = 'http://yangkeduo.com/search_result.html?search_key=iphone%20xr'

# 测试API，选择tester使用哪个测试方法
TEST_METHODS = ['test_single_proxy', 'test_pddsearch_proxy']
TEST_METHOD = TEST_METHODS[1]

# 请求头
DEFAULT_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

# 允许重定向
ALLOW_REDIRECTS = True

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 10
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 5000

# 检查周期
TESTER_CYCLE = 10
# 获取周期
GETTER_CYCLE = 150

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10
