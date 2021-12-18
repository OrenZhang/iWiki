#! /bin/sh

APIDIR=wiki_repo/backend
BASEDIR=/www/wwwroot

# 进入虚拟环境
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Enter VEnv"
cd $BASEDIR/$APIDIR
source $BASEDIR/$APIDIR/venv/bin/activate
echo ""
sleep 2

# 拉取线上最新的内容
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Pull Latest Branch"
git reset --hard HEAD
git pull origin master
echo ""
echo "Git Now At"
git log --oneline | head -n 1
echo ""
sleep 2

# 安装依赖
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Install Modules"
pip install -r requirements.txt
echo ""
sleep 2

# 进行数据库迁移
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Migrate database"
python manage.py migrate
echo ""
sleep 2

# 停止当前所有命令
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Kill All Commands"
ps -ef |grep $APIDIR |awk '{print $2}'|xargs kill -9
echo ""
sleep 5

# 开启新的进程
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Start new uwsgi"
nohup uwsgi --ini $BASEDIR/$APIDIR/uwsgi.ini -w wsgi.wsgi:application > /dev/null 2>&1 &
echo ""
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Start new celery worker"
nohup celery -A modules.cel worker -l INFO -f $BASEDIR/$APIDIR/logs/celery-worker.log > /dev/null 2>&1 &
echo ""
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Start new celery beat"
nohup celery -A modules.cel beat -l INFO -f $BASEDIR/$APIDIR/logs/celery-beat.log > /dev/null 2>&1 &
echo ""
sleep 10

# 检测进程开启结果
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Check Uwsgi"
ps -ef |grep $APIDIR | grep uwsgi
echo ""
echo [$(date "+%Y-%m-%d %H:%M:%S")] "Check Celery"
ps -ef |grep $APIDIR | grep celery
echo ""
