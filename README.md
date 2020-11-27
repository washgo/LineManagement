# 简介
LineManagement主要用于管理云主机，当前管理方式只针对Vultr单一平台，并且只能通过Api的方式进行。后续会添加自定义服务器。

![image](https://github.com/washgo/LineManagement/blob/main/readme1.png)

# 配置
LineManagement可以配置各种服务，服务的添加和删除通过设置文件config/services.json进行。
```json
{
    "Service1":{
        // 服务安装阶段
        "Install":{
            "Config":{
                "Port": "", //服务暴露端口
                "Password": ""  //服务暴露密码,如果需要
            },
            "Command":[
                ""  //需要执行的命令
            ],
            "Generation": {
                "ConfigContent":{ //在本地生成服务的配置文件
                },
                "ShareLink": {  //产生服务的分享信息
                    "Prefix": "", //前缀
                    "Content": "" //内容
                }
            }
        },
        // 启动服务
        "Start":{
            "Config":{
                "File": ""  //服务器上对应的配置文件
            },
            "Command":[
                ""  //需要执行的命令
            ]
        },
        //停止服务
        "Stop":{
            "Command":[
                ""  //需要执行的命令
            ]
        }
    }
}
```

# 发布平台
## 目前已打包平台
Windows x64
Windows x86

## 需自行打包平台
Ubuntu x64
MacOS

# 后续
### 添加其它云主机平台
### 添加自定义添加云主机
