# Notara 桌面版

Notara 是装在自己电脑上的 AI 学习伙伴。这里是桌面版的官方安装包与版本说明仓库；应用源码保持私有。

- [官网与版本选择](https://oh-my-student.com/install/)
- [安装包与版本说明（Releases）](https://github.com/TongZi2003/Notara-Desktop-Releases/releases)
- [桌面版问题反馈](https://github.com/TongZi2003/Notara-Desktop-Releases/issues)

## 当前状态

首个 **Windows 10/11 x64 预览版 0.1.0-preview.5** 已提供下载：[安装程序与版本说明](https://github.com/TongZi2003/Notara-Desktop-Releases/releases/tag/v0.1.0-preview.5)。macOS 与 Windows ARM 原生版本暂未公开。

下载 Release 附件中的 `.exe` 安装程序，并阅读版本说明。此预览版没有商业代码签名，Windows 可能显示“未知发布者”或 SmartScreen 提示；请核对官方来源与随包 SHA256 清单，遵守设备管理策略，无需关闭系统安全保护。预览版暂采用手动下载安装更新。

安装器包含默认学习所需运行时，无需预装 DSH、Node.js 或 Git。使用 Bash 命令需要额外配置本机 Docker Linux 引擎与固定执行镜像。

## 模型与资料

桌面版在独立窗口里提供课堂、白板、Vault 与学习计划。模型服务按供应商配置，使用 API Key 或供应商支持的订阅登录；可用模型、额度和费用由供应商决定。相关对话与资料会发送给你选择的模型服务。

学习资料保存在你选择的本地文件夹。桌面版与 DSH 插件版分别维护，目前不提供课堂记录的自动迁移。

## 反馈问题

请在 Issues 中提供应用版本、操作系统、复现步骤和错误信息。提交前移除 API Key、登录凭据和私人学习内容。
