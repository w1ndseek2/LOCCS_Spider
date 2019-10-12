# LOCCS-Spider

## Project Layout

### Project Working Stream

1. 从给定的txt文件中读取url到redis
2. 从redis中取出url，根据url status存入redis
3. loccs_finish的url还会根据raw http content判断是否有登陆表单
4. 并进行一次深度为1的链接提取（域名与父链接相同）
5. 再次存入redis后续递归

spider.py 爬虫主体 多进程(默认10)  
config.py 配置文件 redis密码 logstash端口等  
randomHP.py 随机header 代理池  
myRedis.py Redis 增，删，状态读取

`实际运行的时候只需要将spider.py里level="DEBUG"设置成level="NONE"即可`

## Development

安装依赖 `pip3 install coloredlogs pyredis`  
使用docker启动一个redis `sudo docker run --rm -d --name redis -v ./data:/data -p 6379:6379 redis --requirepass 'your_password'`

url status
- loccs_todo
- loccs_finish 
  - loccs_login_form
- loccs_timeout
- loccs_forbidden
- loccs_error

## TODO

- [ ] 部署上ELK？
- [ ] js rendering?