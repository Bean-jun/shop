# 其他小技巧

### 1、 代码快速渲染
- 老方式
```python
# 直接读取templates中的html文件
from django.template.loader import get_template

from django.template import Context
from django.http import HttpResponse
import datetime


def index(request):
    now = datetime.datetime.now()
    t = get_template("test.html")
    html = t.render(Context({"time": now}))
    return HttpResponse(html)
```
- 较为简单的方式
```python
from django.shortcuts import render
import datetime

def index(request):
    now = datetime.datetime.now()
    return render(request, "test.html", {"time": now})
```

### 2. 会话保持
>浏览器请求服务器是无状态的。无状态指一次用户请求时，浏览器、服务器无法知道之前这个用户做过什么，每次请求都是一次新的请求。无状态的应用层面的原因是：浏览器和服务器之间的通信都遵守HTTP协议。根本原因是：浏览器与服务器是使用Socket套接字进行通信的，服务器将请求结果返回给浏览器之后，会关闭当前的Socket连接，而且服务器也会在处理页面完毕之后销毁页面对象。

- 在客户端存储信息使用Cookie
- 在服务器端存储信息使用Session

#### 2.1 cookie
- 在django中设置需要使用`HttpResponse`对象来`set_cookies`
- cookie是由服务器生成，存储在浏览器端的一小段文本信息。
- cookie的特点：
    - 1)以键值对方式进行存储。
    - 2)通过浏览器访问一个网站时，会将浏览器存储的跟网站相关的所有cookie信息发送给该网站的服务器。request.COOKIES
    - 3)cookie是基于域名安全的。
    - 4)cookie是有过期时间的，如果不指定，默认关闭浏览器之后cookie就会过期。
    
#### 2.2 session
- session存储在服务器端。
- session的特点：
    - 1) session是以键值对进行存储的。
    - 2) session依赖于cookie。唯一的标识码保存在sessionid cookie中。
    - 3) session也是有过期时间，如果不指定，默认两周就会过期。