为了将kibana集成到我们的单点登陆(CAS框架), 使用django做了这个项目. 后来又加入一点简单的权限控制.

当时做这个项目的时候, 还是kibana3, 只有一个前端应用.  
现在kibana4自带nodejs的WEB服务, 熟悉nodejs的同学直接在nodejs的express web框架上面开发可能会更原生态一些.

# 使用

## internal
因为利用了nginx的internal location特征, 所以需要和nginx配合使用.  apache中好像也有类似的功能, 参考[这个apache mod](https://tn123.org/mod_xsendfile/)

internal的说明可以参考[这里](https://www.nginx.com/resources/wiki/start/topics/examples/xsendfile/), 它的简单配置如下:
  
	location /protected/ {
		internal;
		root   /some/path;
	}
这个配置是说, 如果从外部直接访问/protected, 会返回404.   
需要nginx后面的php啊, django啊, 或者cgi啊, 返回的时候带一个header, 比如, X-Accel-Redirect: /protected/iso.img;  nginx就会把用户的请求重定向到/protected/iso.img这里来.  权限控制就可以在后面的php啊, django啊, cgi处理了.


所以这个项目的想法很简单, 静态的kibana页面放在nginx后面.   
到ES的ajax调用被转到django, 做用户权限认证之后, 再用上面说的方法调转到真正的ES restful入口.

## nginx配置示例

```
server {
    listen       80 default_server;

    location = / {
        include uwsgi_params;
        uwsgi_pass unix:///home/childe/app/esproxy/esproxy/uwsgi.sock;
    }
    location = /login.html {
        include uwsgi_params;
        uwsgi_pass unix:///home/childe/app/esproxy/esproxy/uwsgi.sock;
    }
    location = /login {
        include uwsgi_params;
        uwsgi_pass unix:///home/childe/app/esproxy/esproxy/uwsgi.sock;
    }
    location = /logout.html {
        include uwsgi_params;
        uwsgi_pass unix:///home/childe/app/esproxy/esproxy/uwsgi.sock;
    }
    location = /logout {
        include uwsgi_params;
        uwsgi_pass unix:///home/childe/app/esproxy/esproxy/uwsgi.sock;
    }
    location /elasticsearch/ {
        include uwsgi_params;
        uwsgi_pass unix:///home/childe/app/esproxy/esproxy/uwsgi.sock;
    }
    location /es/ {
        internal;
        proxy_pass   http://127.0.0.1:9200/;
    }
    location / {
        alias /home/childe/app/kibana/;
        index index.html;
    }
}
```

## django应用部署


### clone

	git clone git@github.com:childe/esproxy.git

### pip 安装依赖

    pip install -r requirements.txt

### 配置CAS, 如果需要的话

	INSTALLED_APPS += (
	    "django_cas",
	)
	AUTHENTICATION_BACKENDS = (
	    'django.contrib.auth.backends.ModelBackend',
	    'django_cas.backends.CASBackend',
	)
	CAS_LOGOUT_COMPLETELY = True
	CAS_IGNORE_REFERER = True
	CAS_REDIRECT_URL = "/"
	CAS_AUTO_CREATE_USERS = True
	CAS_GATEWAY = False
	CAS_RETRY_LOGIN = True
	CAS_SERVER_URL = 'https://cas.corp.com'

### 配置kibana目录和访问路径等

	KIBANA_DIR = '~/app/kibana'
	ELASTICSEARCH_PROXY = "/elasticsearch"
	ELASTICSEARCH_REAL = "/es"

### 权限控制
	cd esproxy
	cp authorization.example.yml authorization.yml

配置文件示例如下:
以web打头的索引, 只允许childe访问.  以app打头的索引,不允许childe搜索.  默认权限是允许所有用户访问.
    web.*:
        _mapping:
            allow: ["childe"]
            deny: all
        _aliases:
            allow: ["childe"]
            deny: all
        _alias:
            allow: ["childe"]
            deny: all
        _msearch:
            allow: ["childe"]
            deny: all
        _search:
            allow: ["childe"]
            deny: all
    app.*:
        _search:
            deny: ["childe"]
        _msearch:
            deny: ["childe"]

### 配置uwsgi.ini

	[uwsgi]
	chdir=/home/childe/app/esproxy/esproxy
	module=esproxy.wsgi:application
	master=True
	pidfile=/tmp/esproxy.pid
	vacuum=True
	processes=4
	max-requests=100
	socket=/home/childe/app/esproxy/uwsgi.sock
	daemonize=/var/log/esproxy.log

### 启动uwsgi

    python manage.py syncdb
    uwsgi -i uwsgi.ini
