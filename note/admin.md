# 这是后台的笔记


### 1. 后台中列表页控制显示

#### 1.1 注册模型，实现显示 
```python
from django.contrib import admin
from book.models import Author

admin.site.register(Author)
```

#### 1.2 管理页显示
- 使用管理类实现
    
    - 使用注册参数
    - 使用装饰器
```python
from django.contrib import admin
from book.models import Author

# 装饰器
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

# 注册参数
class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)
```
- 控制管理页关键字段
    - list_display 列表中的列
        - 添上对应模型中的类属性即可
        - 类字段修改列名,只要在定义时加入`verbose_name`字段即可
        - 将类中的方法作为列（不可以排序）
            - 直接写方法名即可
            - 想要让方法可以排序需要在模型中将方法名设定为对应字段`方法名.admin_order_field='模型类字段'`
            - 想要修改列名`方法名.short_description=名称`
    - list_per_page 设定每页显示数据量的多少
    - list_filter 右侧过滤器
    - search_fields 查询字段
    - actions_on_top 操作选项的位置--上
    - actions_on_bottom 操作选项位置--下
    
- 编辑管理页关键字段
    - 注意field和fieldset只能单独使用
    - field 显示字段顺序
    - fieldset 分组显示
    ```python
        fields = ['last_name', 'first_name', 'email']
        fieldsets = (
            ('姓氏', {'fields': ['first_name']}),
            ('名称', {'fields': ['last_name']})
        )
    ```
    - 关联对象
        - 在一对多的关系中，可以在一端编辑页面修改多段的内容。将多端的内容嵌入到一段中有两种方式[表格、块]
        - 使用时需要创建一个多端的表格或者块形式的类，并将其在一端中使用
```python
from django.contrib import admin
from book.models import Book, Publisher
# 创建块
class BookStackedInline(admin.StackedInline):
    model = Book
    extra = 2
# 创建表格
class BookTabularInline(admin.TabularInline):
    model = Book
    extra = 2
    
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    # 使用块方式
    inlines = [BookStackedInline]
    # 使用表格
    inlines = [BookTabularInline]
```
