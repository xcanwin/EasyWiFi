# EasyWiFi
## 简介
```
这是一款抢连wifi工具.
由于无线路由器的连接设备数量有限, 以至于经常发生需要与朋友抢连wifi的情况, 在无法连接路由器时, 若有人刚好掉线, 则本工具可以辅助使用者立刻连上, 因此这是一个悲伤的项目.
原理是基于命令行实现的, 实践表明, 通过命令行来连wifi非常节约连接时间.
```

## 用法
```
配置好intervalTime、interface、ssid、password的内容以后
运行脚本 python EasyWiFi.py
```

## 参数含义
```
intervalTime: 连wifi的重试时间
interface   : 无线网卡名称 (有多个无线网卡时建议配
              置. 若为空, 则自动检测并选择第一个无线网卡)
ssid        : wifi名称
password    : wifi密码
```
