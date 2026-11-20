# Notara 桌面版

Notara 是装在自己电脑上的 AI 学习伙伴。这里是桌面版的官方安装包与版本说明仓库；应用源码保持私有。

- [官网与版本选择](https://oh-my-student.com/install/)
- [安装包与版本说明（Releases）](https://github.com/TongZi2003/Notara-Desktop-Releases/releases)
- [桌面版问题反馈](https://github.com/TongZi2003/Notara-Desktop-Releases/issues)

## 当前状态

面向首轮内测的 **macOS Apple Silicon (`arm64` DMG)** 与 **Windows 10/11 (`x64` Setup.exe)** 预览版 `0.1.0-preview.7` 均已提供下载：[安装程序与版本说明](https://github.com/TongZi2003/Notara-Desktop-Releases/releases/tag/v0.1.0-preview.7)。Windows ARM 原生版与 Intel Mac 公证版暂未发布。

- **macOS 首次启动提示**：本内测包采用本地 ad-hoc 签名、暂未绑定 Apple 公证，打开 DMG 将 `Notara.app` 拖入「应用程序」后，若提示「无法验证开发者 / 未打开」，请先核对随包 `SHA256SUMS.txt` 校验和，再在终端执行 `xattr -cr /Applications/Notara.app`（或在「系统设置 -> 隐私与安全性」点击「仍要打开」）。
- **Windows 首次启动提示**：本预览版没有商业代码签名，Windows 若弹出“未知发布者”或 SmartScreen 提示，请先核对随包 `SHA256SUMS.txt` 校验值，再点击「更多信息 -> 仍要运行」（受组织策略严格管控的电脑可能拦截未签名程序）。预览版暂采用手动下载安装更新。

安装器包含默认学习、PDF 渲染及离线公式字体所需运行时，无需预装 DSH、Node.js 或 Git。使用 Bash 命令需要额外配置本机 Docker Linux 引擎与固定执行镜像。

## 模型与资料

桌面版在独立窗口里提供课堂、白板、Vault 与学习计划。模型服务支持免注册 BYOK，使用自有 API Key 或供应商支持的订阅登录；拆解带配图或手写扫描件 PDF 时，请在「设置 -> 模型连接 / 工作员算力」为拆书整理师与分片建卡员配置带「视觉」标识的模型。可用模型、额度和费用由供应商决定，相关对话与资料会直接发送到你选择的模型服务。

学习资料均保存在你选择的本地文件夹（标准 `.md` 与 `.canvas`）。桌面版与 DSH 插件版分别维护，目前不提供课堂记录的自动迁移。

## 反馈问题

请使用应用内「设置 -> 外观与常用连接 -> 问题反馈与诊断 -> 导出脱敏诊断」获取 JSON 报告，并在 Issues 中附上应用版本、系统版本、复现步骤与报错摘要。提交前请确认已移除 API Key、登录凭据与私人学习内容。
