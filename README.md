### 让你的fastapi穿上django的外衣

#### 实现目标
1. 命令管理
2. 配置式路由
3. 基于SQLModel，更像django的异步ORM
4. 多app协同
5. 公共配置管理

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
