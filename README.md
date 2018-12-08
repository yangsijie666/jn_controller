1. 编辑config.json文件：

    ```json
    {
      "tfn2k":      # tfn2k攻击相关参数配置
      {
        "status":"off",     # "off"即为不启用，"on"即为启用
        "args":
        {
          "time_last":60,       # 整个大周期时间(s)
          "attack_interval":8,  # 小周期中攻击时间(s)
          "wait_interval":2,    # 小周期中不攻击的时间(s)
          "phy_interface":
          {
            "name":"ens33",     # 攻击报文出接口
            "bandwidth":100     # 带宽(Mbps)
          },
          "packet_size":1399,   # 数据包大小(1399bit)
          "flood_type":1,       # 攻击方式：(1-UDP, 2-TCP/SYN, 3-ICMP/PING, 4-ICMP/SMURF, 5-MIX, 6-TARGA3)
          "victims":["10.0.0.1", "10.0.0.2"]    # 攻击目标
        }
      },
      "routetable":     # 路由表采集相关参数配置
      {
        "status":"off",     # "off"即为不启用，"on"即为启用
        "args":
        {
          "time_last":60,       # 整个大周期时间(s)
          "time_interval":1     # 每次探测之间的时间间隔
        }
      },
      "packagecap":     # 数据报采集相关参数配置
      {
        "status":"off",     # "off"即为不启用，"on"即为启用
        "args":
        [                   # 可以同时采集多个端口的数据报
          {
            "interface":"lo",   # 采集的目标端口
            "protocol":"",      # 采集的数据报类型("icmp", "tcp", "udp", "":代表采集所有类型数据报)
            "time_last":60      # 采集持续时间
          },
          {
            "interface":"ens33",
            "protocol":"icmp",
            "time_last":60
          }
        ]
      }
    }
    ```

2. 后台执行监听程序：

    ```bash
    nohup python main.py &
    ```

3.  启动：

    ```bash
    curl -X GET http://127.0.0.1:1227/start
    ```

4. 停止：

    ```bash
    curl -X GET http://127.0.0.1:1227/stop
    ```

