# tmtoolGU
工具集合

### 安装(Python 版本>=3.6.8)
```
pip install --upgrade GUToolsP
```

### 使用

#### 发送邮件
```
from GUTOOLS.tools import Tool
tool = Tool()

tool.mail_from_user_host = '发件地址host'
tool.mail_from_user = '发件人邮箱号'
tool.mail_from_user_pwd = '发件人密码'

tool.send_mail_msg(to_user='收件人邮箱地址（这里是列表，可填写多个）', title='邮件标题', content='邮件内容')
```
#### 数据格式转换
```
from GUTOOLS.tools import Tool
tool = Tool()
tool.json_change(json/dict/其他类型数据)
```
#### url拼接
```
from GUTOOLS.tools import Tool
tool = Tool()
tool.url_sp(url,data)
```

#### http请求（get、post、put、delete、head、patch、options）
```
from GUTOOLS.tools import Tool
tool = Tool()
tool.http_request(type, url ,**kwargs)
```
