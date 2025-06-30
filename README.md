# Ubuntu系统备份工具

版本：2.0.0
最后更新：2025-06-30

一个用于Ubuntu系统间备份和恢复的工具，支持Firefox配置、VirtualBox虚拟机和系统文件的备份。

## 功能特点

- 增量备份（使用rsync）
- 自动备份版本管理
- 备份文件完整性验证
- 详细的进度显示
- 完整的日志记录
- 配置管理
- 错误处理和恢复

## 系统要求

- Ubuntu操作系统
- Python 3.8+
- rsync
- root权限

## 安装步骤

1. 安装依赖：
```bash
python3 -m pip install -r requirements.txt
```

2. 配置设置：
编辑 `config/settings.py` 文件，根据需要修改：
- 源路径和目标路径
- 备份保留策略
- 磁盘型号
- 日志设置

## 使用方法

1. 执行备份（在源机器上）：
```bash
sudo python3 main.py --backup
```

2. 执行恢复（在目标机器上）：
```bash
sudo python3 main.py --restore
```

## 上传代码到GitHub的步骤

1. 创建SSH密钥（如果还没有）：
```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
# 按回车接受默认文件位置
# 可以设置密码短语，也可以直接回车跳过
```

2. 将SSH密钥添加到GitHub：
- 复制公钥内容：
```bash
cat ~/.ssh/id_ed25519.pub
```
- 访问GitHub网站 -> 点击头像 -> Settings
- 点击左侧 "SSH and GPG keys"
- 点击 "New SSH key"
- 给密钥起个名字（如"我的Ubuntu电脑"）
- 粘贴公钥内容并保存

3. 测试SSH连接：
```bash
ssh -T git@github.com
# 首次连接会提示确认，输入yes
```

4. 在GitHub上创建新仓库：
- 访问GitHub网站 -> 点击右上角"+"
- 选择"New repository"
- 填写仓库名（如"backup-system"）
- 选择公开或私有
- 不要初始化README
- 点击"Create repository"

5. 初始化本地Git仓库：
```bash
cd backup_system
git init
git add .
git commit -m "初始提交：完整的备份系统实现"
```

6. 添加远程仓库并推送：
```bash
git remote add origin git@github.com:你的用户名/backup-system.git
git branch -M main
git push -u origin main
```

## 目录结构

```
backup_system/
├── config/           # 配置文件
├── core/            # 核心功能模块
├── logs/            # 日志目录
├── README.md        # 说明文档
├── requirements.txt # 项目依赖
└── main.py         # 主程序入口
```

## 注意事项

1. 确保在执行备份/恢复操作前有足够的磁盘空间
2. 定期验证备份的完整性
3. 保持配置文件的正确性
4. 注意权限要求，必须使用root权限运行
5. 必须使用python3运行程序，使用python2可能会导致错误

## 问题反馈

如果遇到问题或有改进建议，请在GitHub上提交Issue。

## 许可证

MIT License
