### 让你的fastapi穿上django的外衣

#### 实现目标
1. 命令管理
2. 配置式路由
3. 基于SQLModel，更像django的异步ORM
4. 多app协同
5. 公共配置管理
6. 接入蓝鲸体系

#### 已实现
1. 命令管理    100%
2. 配置式路由1.0    100%
3. ORM    30%
4. 多app协同    10%
5. 公共配置管理  5%

#### 如何启动?

首先修改settings.py中相关配置项
1. 创建sqlite3数据库: python app.py mkdb
2. 启动server：python app.py runserver [ip] [port]

#### 添加第一个app

1. 在项目根目录新增一个子目录demo
2. 在demo下新增urls.py和api.py
3. 在urls.py中新增:
    ```
    from demo.api import demo_api
    url_pattern = [("/",demo_api, ["get"]),]
    ```
4. 在api.py中新增demo_api函数:
    ```
    def demo_api():
        return "ok"
    ```
5. 执行python app.py runserver
6. 访问:http://127.0.0.1:8000/docs/ 使用swargger进行一个try it吧