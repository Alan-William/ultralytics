# 🐛 树莓派系统内存优化笔记

> **日期**: 2026-03-13  
> **设备**: Raspberry Pi 5 (4GB RAM)  
> **问题**: 系统定时重启/崩溃  
> **解决方案**: 增加交换空间

---

## 📋 问题描述

### 现象
- 系统运行约 40-60 分钟后自动重启
- 无明显触发条件，看似"定时"重启
- OpenClaw Gateway 服务频繁重启

### 初步诊断
```bash
# 检查系统启动记录
journalctl --list-boots

# 检查系统日志
journalctl --since "2026-03-13 00:00:00" --priority=3 --no-pager

# 查看内存使用
free -h
ps aux --sort=-%mem | head -10
```

---

## 🔍 根本原因

### OOM (Out of Memory) 崩溃

**证据：**
```
3 月 13 18:29:35 kernel: Out of memory: Killed process 2662 (Isolated Web Co)
total-vm:5422896kB, anon-rss:1286304kB
```

**内存占用分析：**

| 进程 | 内存占用 | 占比 |
|------|---------|------|
| OpenClaw Gateway | 735MB | 17.7% |
| Firefox 浏览器 | 240MB | 5.8% |
| 其他系统进程 | ~800MB | 20% |
| **总计** | **~1.8GB** | **45%** |

**问题链：**
1. 树莓派仅有 4GB 物理内存
2. 长时间运行后内存逐渐耗尽
3. 交换空间不足（仅 2GB）
4. 触发 OOM Killer 强制杀死进程
5. 关键服务崩溃导致系统重启

---

## ✅ 解决方案

### 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **增加交换空间** | 简单、无副作用、立即生效 | 轻微性能损失 | ⭐⭐⭐⭐⭐ |
| 限制应用内存 | 精确控制 | 可能影响功能 | ⭐⭐⭐ |
| 监控 + 自动重启 | 主动管理 | 需要额外脚本 | ⭐⭐⭐⭐ |

### 实施：增加 2GB 交换空间

#### 步骤 1：创建交换文件
```bash
sudo fallocate -l 2G /swapfile2
```

#### 步骤 2：设置安全权限
```bash
sudo chmod 600 /swapfile2
```

#### 步骤 3：格式化为 swap
```bash
sudo mkswap /swapfile2
```

#### 步骤 4：启用交换空间
```bash
sudo swapon /swapfile2
```

#### 步骤 5：设置开机自启
```bash
echo '/swapfile2 none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 📊 优化效果

### 优化前后对比

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **总交换空间** | 2.0GB | 4.0GB | **+100%** |
| **可用交换空间** | 1.3GB | 3.3GB | **+154%** |
| **可用内存** | 613MB | 1.3GB | **+112%** |
| **系统稳定性** | 40 分钟崩溃 | 持续运行 | **显著改善** |

### 验证命令
```bash
# 查看内存状态
free -h

# 查看交换空间详情
cat /proc/swaps

# 查看交换空间优先级
swapon --show
```

---

## 🧠 知识点总结

### 1. OOM (Out of Memory) 机制

**什么是 OOM Killer？**
- Linux 内核在内存耗尽时的自我保护机制
- 强制杀死占用内存最多的进程
- 通过 `oom_score_adj` 决定杀死优先级

**查看 OOM 日志：**
```bash
journalctl --grep="Out of memory\|OOM\|killed process" --no-pager
dmesg | grep -i "out of memory"
```

### 2. 交换空间 (Swap)

**作用：**
- 当物理内存不足时，将部分数据临时存储到磁盘
- 避免 OOM 崩溃
- 允许运行更多应用

**性能权衡：**
- Swap 速度远慢于 RAM（约 100-1000 倍）
- 频繁使用 swap 会导致系统变慢（swap thrashing）
- 但比崩溃好得多

**推荐配置：**
| 物理内存 | 推荐 Swap |
|---------|-----------|
| 2GB | 4GB |
| 4GB | 4-8GB |
| 8GB | 4GB |
| 16GB+ | 2-4GB |

### 3. 内存监控命令

```bash
# 实时查看内存
htop
free -h
watch -n 1 free -h

# 查看进程内存占用
ps aux --sort=-%mem | head -20
top -o %MEM

# 查看内存详细信息
cat /proc/meminfo

# 查看特定进程内存
ps -p <PID> -o pid,rss,vsz,%mem,cmd
```

### 4. Systemd 服务管理

```bash
# 查看服务状态
systemctl status openclaw

# 查看服务重启历史
systemctl status openclaw | grep -A5 "restart"

# 查看服务日志
journalctl -u openclaw --no-pager -n 50

# 重启服务
sudo systemctl restart openclaw

# 禁用服务
sudo systemctl disable <service-name>
```

### 5. 定时任务检查

```bash
# 用户定时任务
crontab -l

# 系统定时任务
ls -la /etc/cron.*
systemctl list-timers --all

# 查看定时任务日志
journalctl -u cron --no-pager
```

---

## 🛠️ 实用脚本

### 内存监控脚本
```bash
#!/bin/bash
# ~/workspace/scripts/monitor_memory.sh

LOG_FILE=~/memory_log.txt
MEM_LIMIT=800  # MB

# 获取 OpenClaw 内存占用
OPENCLAW_PID=$(pgrep -f openclaw-gateway)
if [ -n "$OPENCLAW_PID" ]; then
    MEM=$(ps -p $OPENCLAW_PID -o rss= | awk '{print int($1/1024)}')
    echo "$(date): OpenClaw - ${MEM}MB" >> $LOG_FILE
    
    # 超限时告警
    if [ $MEM -gt $MEM_LIMIT ]; then
        echo "⚠️ WARNING: OpenClaw memory exceeds ${MEM_LIMIT}MB" >> $LOG_FILE
    fi
fi
```

### 自动清理缓存
```bash
#!/bin/bash
# ~/workspace/scripts/clean_cache.sh

# 清理页面缓存、dentries 和 inodes
sudo sync
sudo sysctl -w vm.drop_caches=3
echo "$(date): Cache cleaned" >> ~/cache_clean.log
```

---

## 📝 最佳实践

### 1. 定期监控
- 每天检查内存使用趋势
- 设置内存告警阈值（80%）
- 记录异常事件

### 2. 应用优化
- 限制浏览器标签页数量
- 关闭不必要的后台服务
- 使用轻量级应用替代

### 3. 系统维护
- 每周重启一次（清理内存泄漏）
- 定期更新系统包
- 监控磁盘空间（swap 文件需要空间）

### 4. 故障排查流程
```
1. 检查系统日志 (journalctl)
2. 查看内存使用 (free -h, ps aux)
3. 分析 OOM 事件 (dmesg | grep -i oom)
4. 检查定时任务 (crontab, systemctl list-timers)
5. 监控系统资源 (htop, iotop)
```

---

## 🔗 参考资源

- [Linux OOM Killer 机制](https://www.kernel.org/doc/guides/admin-guide/mm/oom killer.rst)
- [Raspberry Pi 内存优化](https://www.raspberrypi.com/documentation/computers/os.html)
- [Systemd 服务管理](https://www.freedesktop.org/software/systemd/man/systemctl.html)
- [Swap 空间配置指南](https://help.ubuntu.com/community/SwapFaq)

---

## 📅 后续行动

- [ ] 监控一周系统稳定性
- [ ] 如仍有问题，考虑限制 Firefox 内存
- [ ] 添加内存监控告警
- [ ] 定期清理系统缓存

---

**最后更新**: 2026-03-13  
**维护者**: Alan William  
**状态**: ✅ 已解决
