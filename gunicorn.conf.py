import multiprocessing

# 預加載資源
preload_app = True
# 綁定ip
bind = "127.0.0.1:8000"
# 進程數 = cup數量 * 2 + 1
workers = multiprocessing.cpu_count() * 2 + 1
# 線程數 = cup數量 * 2
threads = multiprocessing.cpu_count() * 2
# 等待隊列最大長度,超過長度就拒絕連接
backlog = 2048
# 工作模式--協程
worker_class = "gevent"
# 最大客户客户端併發數量,對使用線程和協程的worker的工作有影響
# 服務器配置(中小型項目):1200
worker_connections = 1200
# 進程名稱
proc_name = 'gunicorn.pid'
# 進程pid紀錄文件
pidfile = 'app_run.log'
# 記錄等級
loglevel = 'debug'
# 紀錄文件名
logfile = 'debug.log'
# 訪問紀錄
accesslog = 'access.log'
# 访问记录格式
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
