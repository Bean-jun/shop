# 这是个模板笔记

    模板是HTML页面，可以根据视图中传递过来的数据进行填充
    创建模板：
        创建templates目录，在目录下创建对应项目的模板目录（project/templates/myApp）
    配置模板路径：
        修改settings.py文件下的TEMPLATES下的'DIRS'为'DIRS': [os.path.join(BASE_DIR, 'templates')],
   
### 1、 基本使用方式
```python
from django.template import Template, Context

text = Template("this is template, i'm {{name}}")
content = Context({"name":"小白"})
text.render(content)
```
### 2、变量
- 变量传递给模板的数据
  
        要遵守标识符规则, 注意一定以字母开头
        语法 {{ var }}
        注意：如果使用的变量不存在，则自动插入的是空字符串

- 在模板中使用点语法
  
        点号可以访问字典的键、属性、方法或对象的索引
            字典查询
            属性或者方法
            数字索引
- 在模板中调用对象的方法
  
        注意：在模板里定义的函数不能传递self以外的参数
- 上述三种方式举例
```python
from django.template import Template, Context

# 使用变量传递
text = Template("this is template, i'm {{name}}")
content = Context({"name":"小白"})
text.render(content)

# 使用点语法
pc_info_dict = {"cpu":"i3", "disk":"东芝", "display":"apple"}
pc_info_list = ["i3", '东芝']
class PersonComputer:
    def __init__(self):
        self.cpu = 'i3'
        self.disk = '东芝'
        self.display = "apple"

# 字典
text = Template("pc have {{info.cpu}} cpu, {{info.disk}} disk")
content = Context({"info": pc_info_dict})
text.render(content)

# 列表
text = Template("pc have {{info.0}} cpu, {{info.1}} disk")
content = Context({"info": pc_info_list})
text.render(content)

# 对象
text = Template("pc have {{info.cpu}} cpu, {{info.disk}} disk")
content = Context({"info": PersonComputer()})
text.render(content)
```

### 3、标签
- 3.1 if 标签
    - 计算变量的值，如果为真（即存在、不为空，不是假值）
      
    - 支持使用and、or 或not 测试多个变量，或者取反指定的变量
      
    - 注意：上述的and、or 或not不允许使用(),真遇到了，可以使用嵌套结构
    - 格式1
    
            {% if %}
                内容
            {% endif %}
    - 格式2
        
            {% if %}
                内容
            {% else %}
                内容
            {% endif %}
    - 格式3
            
            {% if %}
                内容
            {% elif %}
                内容
            {% elif %}
                内容
            ...
            {% else %}
                内容
            {% endif %}
    
- 3.2 for 标签
    - 用于迭代序列中的各个元素
    
    - 格式1
      
            {% for 变量 in Python对象 %}
                语句
            {% endfor %}
    - 格式2
      
            {% for 变量 in Python对象 %}
                语句
            {% empty %}  # 注意：列表为空或者列表不存在时执行empty内的内容
                语句2
            {% endfor %}
    - 格式3

            {{ forloop.counter }}
    
- 3.3 ifequal/ifnotequal 标签
    - 标签比较两个值，如果相等/不相等，显示内部的内容
    - 本质上可以使用if 和 ==/!= 来替代
    - 格式
        
            {% ifequal user currentuser %}
                内容
            {% endifequal %}
    
- 3.4 注释
    - 用来注释代码，让其不显示
    - 注释不可以嵌套
      
    - 单行注释：
      
            {# 被注释的内容 #}
    - 多行注释
      
            {% comment %}
                注释内容
            {% endcomment %}
    
- 3.5 include 
    - 加载模板并以标签内的参数渲染
    - 格式：
      
            {% include '模板目录' 参数1 参数2 %}
    
### 4、过滤器

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;模板过滤器是在显示变量之前调整变量值的简单方式。过滤器使用管道符号指定

- 基本格式
    
        语法 {{ var|过滤器 }}
- 示例：
  
        过滤器可以传递参数，参数用引号引起来
            join 格式 列表|join:"#"
                 示例：{{list1|join:"#"}}
        如果一个变量没有被提供，或者值为false,空，我们可以通过 default 语法使用默认值
            格式： {{str1|default:"没有"}}
        根据给定格式转换日期为字符串：date
            格式： {{dateVal|date:'y-m-d'}}
        HTML转义：escape
            
            举例：
                问题：return render(request, 'myApp/index.html', {"code": "<h1>sunck is a very good man</h1>"})中的{{code}}
                  {{code}}里的code被当作<h1>sunck is a very good man</h1>显示，未经过渲染
                解决方法：
                    {{code|safe}}
                或  {% autoescape off %}
                        {{code}}
                    {% endautoescape %}  # 这个可以一口气解决一堆

### 5、 模板
- 模板继承可以减少页面的重复定义，实现页面的重用
- block标签：在父模板中预留区域 ，子模板去填充
- 语法 ： 
  
        {% block 标签名 %}
  
        {% endblock 标签名 %}
- extends标签：继承模板，需要写在模板文件的第一行
- 语法 ： 
    
        {% extends 'myApp/base.html' %}
        {% block main %}
            内容
        {% endblock 标签名 %}
- 示例：
  
            定义父模板
                body标签中
                {% block main %}

                {% endblock main %}

                {% block main2 %}

                {% endblock main2 %}
            定义子模板
                {% extends 'myApp/base.html' %}
                {% block main %}
                    <h1>sunck is a good man</h1>
                {% endblock main %}

                {% block main2 %}
                    <h1>kaige is a good man</h1>
                {% endblock main2 %}


### 6、反向解析
- 在模板中需要将href设置为{% url "namespace:name" %}
```markdown
在模板文件中使用时，格式如下:
{% url 'namespace名字：name' %} 例如{% url 'booktest:fan2'%}
带位置参数：
{% url 'namespace名字：name' 参数 %} 例如{% url 'booktest:fan2' 1%}
带关键字参数：
{% url 'namespace名字：name' 关键字参数 %} 例如{% url 'booktest:fan2' id=1 %}
```
- 在视图中的操作
```markdown
在重定向的时候使用反向解析：
from django.core.urlresolvers import reverse
无参数：
reverse('namespace名字:name名字')
如果有位置参数
reverse('namespace名字:name名字', args = 位置参数元组)
如果有关键字参数
reverse('namespace名字:name名字', kwargs=字典)
```