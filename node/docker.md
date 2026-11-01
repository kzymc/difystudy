## 一、镜像（Image）管理命令

### ✅ 查看与搜索

- `docker images` / `docker image ls` — 查看本地镜像
- `docker search <name>` — 搜索镜像
- `docker inspect <image>` — 查看镜像详情
- `docker history <image>` — 查看镜像历史

### ✅ 拉取与推送

- `docker pull <image>:<tag>` — 拉取镜像
- `docker push <image>` — 推送镜像到仓库
- `docker login` / `docker logout` — 登录/退出仓库 

### ✅ 构建与标记

- `docker build -t <name>:<tag> .` — 构建镜像
- `docker build --no-cache -t <name> .` — 不使用缓存构建 
- `docker tag <src> <target>:<tag>` — 镜像打标签

### ✅ 删除与清理

- `docker rmi <image>` — 删除镜像
- `docker image prune -a` — 清理未使用镜像 

------

## 二、容器（Container）管理命令

### ✅ 查看容器

- `docker ps` — 查看运行中容器
- `docker ps -a` — 查看所有容器 
- `docker inspect <container>` — 查看容器详情
- `docker stats` — 查看资源使用

### ✅ 启动 / 停止 / 删除

- `docker start <id>` — 启动容器
- `docker stop <id>` — 停止容器
- `docker restart <id>` — 重启容器
- `docker rm <id>` — 删除容器

### ✅ 运行容器

- `docker run -d <image>` — 后台运行
- `docker run -p 8080:80 <image>` — 端口映射
- `docker run -v host:container <image>` — 挂载卷
- `docker run --restart=always <image>` — 设置重启策略 

- `docker exec -it <id> bash` — 进入容器
- `docker exec <id> <cmd>` — 在容器中执行命令

### ✅ 日志

- `docker logs <id>` — 查看日志
- `docker logs -f <id>` — 实时日志

### ✅ 文件复制

- `docker cp <container>:/path /host` — 容器 → 主机
- `docker cp /host <container>:/path` — 主机 → 容器

------

## 三、网络（Network）管理命令

- `docker network ls` — 查看网络 
- `docker network inspect <name>` — 查看网络详情
- `docker network create <name>` — 创建网络
- `docker network rm <name>` — 删除网络
- `docker network connect <network> <container>` — 容器加入网络

------

## 四、数据卷（Volume）管理命令

- `docker volume ls` — 查看卷
- `docker volume create <name>` — 创建卷
- `docker volume rm <name>` — 删除卷 
- `docker volume inspect <name>` — 查看卷详情

------

## 五、Docker Compose 常用命令

（适用于 docker-compose.yml 所在目录）

### ✅ 启动 / 停止

- `docker compose up -d` — 后台启动服务
- `docker compose down` — 停止并删除服务
- `docker compose stop` — 停止但不删除

### ✅ 构建 / 查看

- `docker compose build` — 构建镜像
- `docker compose ps` — 查看服务状态
- `docker compose logs -f` — 实时日志

------

## 六、系统与清理命令

- `docker version` — 查看版本
- `docker info` — 查看系统信息 
- `docker system df` — 查看磁盘占用
- `docker system prune` — 清理未使用资源
- `docker system prune -a` — 深度清理（含未使用镜像）

------

## 七、常用组合命令（高频）

- 停止所有容器：
  `docker stop $(docker ps -q)`
- 删除所有容器：
  `docker rm -f $(docker ps -aq)`
- 删除所有镜像：
  `docker rmi $(docker images -q)`