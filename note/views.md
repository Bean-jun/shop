# 这是视图的笔记


### 1. URLConf
- URL获取值
    - 请求的url被看做是一个普通的python字符串，进行匹配时不包括域名、get或post参数。
    - 在这部分中，URL设置正则即可，会传递给对应的视图函数。
> 具体获取参数方式
>  - 位置参数
>      - 使用小括号将对应正则框柱即可
>      - exp:`url(r'^index(\d+)/$',views.index),`
>  - 关键字参数
>      - 正则表达式部分为组命名
>      - exp:`url(r'^index(?P<id1>\d+)/$',views.index),`
>      - 注意上述例子中，index视图函数中参数名必须是`id1`


### 2. HttpResponse对象
- 属性
    - path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
    - method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
    在浏览器中给出地址发出请求采用get方式，如超链接。
    在浏览器中点击表单的提交按钮发起请求，如果表单的method设置为post则为post请求。
    - encoding：一个字符串，表示提交的数据的编码方式。
    如果为None则表示使用浏览器的默认设置，一般为utf-8。
    这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。
    - GET：QueryDict类型对象，类似于字典，包含get请求方式的所有参数。
    - POST：QueryDict类型对象，类似于字典，包含post请求方式的所有参数。
    - FILES：一个类似于字典的对象，包含所有的上传文件。
    - COOKIES：一个标准的Python字典，包含所有的cookie，键和值都为字符串。
    - session：一个既可读又可写的类似于字典的对象，表示当前的会话，只有当Django 启用会话的支持时才可用，详细内容见"状态保持"。

#### 2.1 QueryDict对象
- 定义在django.http.QueryDict
- HttpRequest对象的属性GET、POST都是QueryDict类型的对象
- 与python字典不同，QueryDict类型的对象用来处理同一个键带有多个值的情况
- 方法get()：根据键获取值
- 如果一个键同时拥有多个值将获取最后一个值
- 如果键不存在则返回None值，可以设置默认值进行后续处理
- 方法getlist()：根据键获取值，值以列表返回，可以获取指定键的所有值
- 如果键不存在则返回空列表[]，可以设置默认值进行后续处理

### 3. HttpResponse对象
- 视图在接收请求并处理后，必须返回HttpResponse对象或子对象。在django.http模块中定义了HttpResponse对象的API。HttpRequest对象由Django创建，HttpResponse对象由开发人员创建。

#### 3.1 JsonResponse
- 在浏览器中使用javascript发起ajax请求时，返回json格式的数据，此处以jquery的get()方法为例。类JsonResponse继承自HttpResponse对象，被定义在django.http模块中，创建对象时接收字典作为参数。
  - 由于ajax请求是一个异步操作，若是需要同步操作，可以在ajax中加入`'async':flase`即可

#### 3.2 HttpResponseRedirect
- 当一个逻辑处理完成后，不需要向客户端呈现数据，而是转回到其它页面，如添加成功、修改成功、删除成功后显示数据列表，而数据的列表视图已经开发完成，此时不需要重新编写列表的代码，而是转到这个视图就可以，此时就需要模拟一个用户请求的效果，从一个视图转到另外一个视图，就称为重定向。

- Django中提供了HttpResponseRedirect对象实现重定向功能，这个类继承自HttpResponse，被定义在django.http模块中，返回的状态码为302。
