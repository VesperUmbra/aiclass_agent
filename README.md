# 大作业计划

## 使用方法（10.30update）

CLI启动：运行`CLI_main.py`，参照测试用例（e.g.：搜索港股昨天市值最高的科技类股票的名称，并进行分析）的语句输入指令开始运行。每次运行只允许输入一次指令，要输入多条指令的话，可以选择反复运行。

前端启动：运行`api_server.py`，然后访问`http://127.0.0.1:5000/`，在输入框中输入指令，点击“开始分析”开始运行。

~~一定要在CLI和前端之间选一个用的话，那么不推荐使用前端~~

测试指令保存在：`测试_指令.md`

注意事项：`yfinance`库使用的数据源雅虎财经访问不稳定，最好使用魔法上网访问（代码中默认使用），且对A股数据支持可能一般，搜索时建议聚焦港股美股进行分析，指令最好能够使智能体确定指向 ***1支*** 股票，且 ***不能是*** 指数（如：日经225、纳斯达克指数、恒生指数等，测试时发现指数类股票无法正常进行解析）。本工具默认的代理端口为7890（保存在`.env`中），请参照自身魔法上网工具配置进行调整，否则可能发生大模型API连接超时等错误。

## 基本环境配置
*参考文档：https://microsoft.github.io/autogen/stable/index.html*

虚拟环境基准：python 3.12

需求库：（pip install安装） 

`autogen-agentchat`

`autogen-ext[openai]`

`yfinance`

`matplotlib`

`pytz`

`numpy`

`pandas`

`python-dotenv`

`requests`

`bs4`

`flask`

## 大作业完成计划
多智能体任务：搜索指定范围内的股票价格，作折线图，并对搜索到的结果发表评论，最后把所有内容进行整合输出。

*参考文档：https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/examples/company-research.html*

结构：round-robin-team，按照上述顺序

模型：deepseek，api用`.env`中给的api-key

相应的api和密钥建议放到`.env`中统一管理。


## 开发任务分配 
Main.py编写，其他代码内容整合——1人

前端设计、logging设计——1人

前后端通信——1人

智能体策略编写——各1人（共5人）

测试脚本（5组）编写和测试运行——1人

测试运行并录制demo视频、整合PPT、word、展示——1人

**编写的代码、网页、demo视频都上传到github上**

## 汇报任务分配：
PPT：制作各自负责的部分，其中前端设计者需要同时负责领域综述。
展示共10分钟，每人做1-2页就可以了

Word写作分配同上
