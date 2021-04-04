# 这是模型笔记


### 1、 字段类型及一些小部分操作
- [Models_Field](models_field.txt)


### 2、 字段查询
    此查询类似于SQL中的select查询
#### 2.1 查询集
- all() 返回所有结果
- filter(条件) 返回满足条件的内容
- exclude(条件) 返回满足条件之外的内容
- order_by(字段) 根据字段进行排序

#### 2.2 返回单个值的过滤器
- get() 返回单个值
- count() 返回查询集中的内容个数
- aggregate() 聚合

#### 2.3 返回某个查询集中内容是否存在
- exists() 返回内容是否存在

### 3、条件查询
- exact 判断相等
```python
模型名.objects.filter(pk__exact=1)
或者
模型名.objects.filter(pk=1)
```

- contains 包含xx内容
```python
模型名.objects.filter(字段名__contains="xx")
```

- endswith及startswith 结束和开头包含xx
```python
模型名.objects.filter(字段名__startswith="xx")
模型名.objects.filter(字段名__endswith="xx")
```

- isnull 内容是否为空


- in 内容是否在范围以内


- 比较查询

    - gt 大于
    - gte 大于等于
    - lt 小于
    - lte：小于等于
    
- 日期查询

    - year 年
    - month 月
    - day 天
    - week_day 
    - hour
    - minute
    - second
    
- F对象
    - 用于属性和属性的比较,同时F对象可以参加运算
```python
# 查询阅读量大于等于评论量的图书
from django.db.models import F
Book.objects.filter(readnum_gte = F('commentnum'))
# 查询阅读量大于等于2倍的评论量的图书
Book.objects.filter(readnum_gte = F('commentnum')*2)
```
- Q对象
  - 多个过滤器逐个调用表示逻辑与关系
    - Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或。
    - Q对象前可以使用~操作符，表示非not。
```python
from django.db.models import Q
# 查询阅读量大于20，或编号小于3的图书，只能使用Q对象实现
Book.objects.filter(Q(readnum__gt = 20) | Q(readno__lt = 3))
```

- aggregate 聚合
  - 返回值是字典类型
    - {'聚合类小写__属性名':值}
```python
from django.db.models import Sum, Avg, Count, Max, Min
# 统计Book中title的数量，  下面聚合结果为{'title__count': 2}
Book.objects.aggregate(Count("title"))
```

### 四、 关联查询（类似于SQL中的join）
- 一对多查询
  - 使用对象查询
    - 一对应的对象名.多对应的模型名小写_set.all()
    ```python
    obj = 一模型名.objects.filter(pk=1)
    obj.多模型名_set.all()
    ```
  - 使用类查询
    - 一模型名关联属性名__-模型类属性名=条件
    ```python
    # 多模型名.objects.filter(多模型中对应一模型的字段__-模型类属性名="图灵出版社")
    # 查询图灵出版社所有图书
    Book.objects.filter(publisher__name='图灵出版社')
    ```
  
- 多对一查询
  - 使用对象查询
    - 多对应对象名.多对应的模型类中关系类的属性
    ```python
    obj = 多模型名.objects.filter(pk=1)
    obj.对应属性名
    ```
  - 使用类查询
    - 关联模型类名小写__属性名__条件运算符=条件
    ```python
    一模型名.objects.filter(关联模型类名小写__属性名="天龙八部")
    # 查询天龙八部对应的出版社
    Publisher.objects.filter(book__title="天龙八部")
    ```
    
### 五、 元选项
- 在模型类中定义类Meta，用于设置元信息，如使用db_table自定义表的名字。
```python
class Meta:
    db_table = "bookinfo" # 定义表名
```

### 六、 模型管理器
> 属性objects：管理器，是models.Manager类型的对象，用于与数据库进行交互。

> 当没有为模型类定义管理器时，Django会为每一个模型类生成一个名为objects的管理器，自定义管理器后，Django不再生成默认管理器objects。

> 使用方式
> 1. 创建模型管理器类
> 2. 使用时，需要在对应类中加入模型管理器的实例化对象

- 自定义管理器类主要用于两种情况：
  - 1.修改原始查询集，重写all()方法
  - 2.向管理器类中添加额外的方法，如向数据库中插入数据。

