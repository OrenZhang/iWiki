<img alt="iWiki Logo" height="60" src="./assets/favicon.png">

iWiki 是一个知识共享平台，也可用作个人博客。依赖 `Python 3.9` + `Node.js 16.13.1` + `Vue 3` + ···  

![wiki.incv.net_(Laptop).png](./assets/wiki.incv.net_(Laptop).webp)

## 部署

由于 iWiki 为前后端分离开发与部署项目，并使用到了腾讯云的部分服务，首次部署的步骤、耗时较多，可以邮件至 `incv2020@outlook.com` 协助部署。

## 部署前端

### 1. 在 `/frontend/src/context` 目录，修改网站网址

修改 `prod.js` 文件，将对应的网址修改为自己的网址。   
`siteUrl` 是前端地址，结尾有斜杠，只支持网站根目录部署，`backEndUrl` 是后端地址，结尾没有斜杠。

```js
export const prodConfig = {
    siteUrl: 'https://wiki.incv.net/',
    backEndUrl: 'https://api.wiki.incv.net'
}
```

### 2. 在 `/frontend` 目录，构建前端文件

```bash
yarn install && yarn build
```

### 3. NGINX 配置静态网站访问，运行网站

具体配置步骤请自行完成。

## 部署后端

### 1. 在 `/backend/entry` 目录，修改后端配置

复制 `settings_tpl.json` 为 `settings.json` 并根据实际情况进行配置。   
如果不配置腾讯云相关的接口，那么将无法使用对应的服务，如短信服务(注册，重置密码等),对象存储(照片、文件上传等)。
本地注册用户可以使用 Django 的 `createsuperuser` 的形式进行注册。

- DEBUG: 调试模式
- SERVICE_CLOSED: 关闭所有服务
- APP_SECRET_KEY: 密钥，可以使用UUID随机生成，初始化后不可更改
- BACKEND_HOST: 后端地址，需要和前端在同一根域名下
- FRONTEND_URL: 前端地址，需要和后端在同一根域名下
- SESSION_COOKIE_DOMAIN: 建议设置为根域名
- DB_NAME: 数据库名
- DB_USER: 数据库用户
- DB_PASSWORD: 数据库密码
- DB_HOST: 数据库 host
- DB_PORT: 数据库端口
- REDIS_HOST: Redis Host
- REDIS_PORT: Redis 端口
- REDIS_PASSWORD: Redis 密码，无密码则为空字符串
- REDIS_DB: Redis 库
- TCLOUD_*: 腾讯云密钥配置(非必须)
- SMS_*: 腾讯云短信配置(非必须)
- COS_*: 腾讯云对象存储配置(非必须)
- DEFAULT_REPO_NAME: 默认库的库名

### 2. 在 `/backend` 目录，修改后端运行配置

修改 `uwsgi.ini` 文件，按照实际情况进行修改。

### 3. 在 `/backend` 目录，安装依赖

```bash
pip install -r requirements.txt

pip install uwsgi
```

### 4. 在 `/backend` 目录，执行数据库变更

```bash
python manage.py migrate
```

### 5. 在 `/backend` 目录，重启相关进程

此步需要根据实际配置进行调整，`APIDIR` 为后端目录(含父级目录), `BASEDIR` 为项目跟目录的父级目录，使用 `BASEDIR` 和 `APIDIR` 拼接可以得到后端目录。

```bash
APIDIR=wiki_repo/backend
BASEDIR=/www/wwwroot
ps -ef |grep $APIDIR |awk '{print $2}'|xargs kill -9
nohup uwsgi --ini $BASEDIR/$APIDIR/uwsgi.ini -w wsgi.wsgi:application > /dev/null 2>&1 &
nohup celery -A modules.cel worker -l INFO -f $BASEDIR/$APIDIR/logs/celery-worker.log > /dev/null 2>&1 &
nohup celery -A modules.cel beat -l INFO -f $BASEDIR/$APIDIR/logs/celery-beat.log > /dev/null 2>&1 &
```

### 6. 配置 NGINX 反向代理访问

具体配置步骤请自行完成。

## 部署完成

至此，部署已经完成，请分别测试前后端域名是否能正常访问。
