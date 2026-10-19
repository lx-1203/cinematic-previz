# cinematic-previz · 漫剧导演与 Updream 工作流

把剧本、导演分镜、Blender 白模预演、首帧与真实视频尾帧接力放在同一个 Skill 中。也可只用 Updream MCP 插件处理节点和多个聊天的协作，不必启动整套影片制作。

## 主要内容

| 入口 | 内容 |
| --- | --- |
| [SKILL.md](SKILL.md) | 调用前更新、任务路由、导演与镜头接力流程 |
| [Updream 使用指南](references/updream-mcp.md) | 连接、多工作区认领、节点操作、生成状态及错误恢复 |
| [30 个接口与示例](references/updream-tools.md) | MCP 参数格式与调用示例，实例 ID 为虚构值 |
| [初始提示词](references/updream-prompts.md) | 只读初始化、节点任务、视频制作和跨聊天交接 |
| [界面补充](references/updream-ui.md) | 上传、本地素材、角色库与未覆盖设置 |
| [来源和许可证](references/sources.md) | 整合来源、提交与上游许可 |

Updream 的 MCP 工具由单独的 Updream MCP Bridge 提供；安装这个 Skill 不会自动安装浏览器扩展、注册 MCP 或连接账号。接口说明以 Bridge 0.3.0 为依据，运行时实际工具目录为准。

## 安装并注册项目来源

需要 Python 3.11+。克隆本仓库后，用真实绝对路径替换下面两个路径：

```powershell
git clone https://github.com/lx-1203/cinematic-previz.git
python "<克隆项目路径>/scripts/sync_from_project.py" --project-root "<克隆项目路径>" --target "<Codex技能目录>/cinematic-previz" --register
```

Codex 技能目录使用本机配置的 CODEX_HOME/skills；首次安装也可按当前宿主支持的技能目录设置。同步目标必须独立于来源目录，不能把克隆目录本身再当安装目标。已有安装首次注册会备份被替换的文件；后续独立修改会触发冲突保护。

也支持来源是一个较大的项目，其 Skill 位于 `skills/cinematic-previz/`：把 --project-root 指向该项目根即可。安装端注册文件记录真实路径；公开源码不写死开发者的机器路径。

## 每次调用前自更新

每次使用前先运行安装目录中的脚本，再重新读取更新后的 SKILL.md 和任务参考：

```powershell
python "<Codex技能目录>/cinematic-previz/scripts/sync_from_project.py"
```

Skill 的首个步骤已要求执行此检查。本机还可在 AGENTS.md 中限定该 Skill：使用前先运行上面命令，成功后加载最新版，失败时停止该 Skill 的业务步骤。这里实现的是可执行同步脚本及调用入口约定，不假定宿主有未配置的专用 Skill 更新 hook。官方关于 Skill 指令与脚本的说明见 [Build skills](https://developers.openai.com/plugins/build/skills)。

| 结果 | 意义和处理 |
| --- | --- |
| current | 安装内容与本次检查的项目版本一致，可继续 |
| updated | 已更新；重新读取 skill_file；若脚本自身更新，再检查一次 |
| update_available | 仅 --check 比较模式，不代表已经更新 |
| LOCAL_CONFLICT | 安装副本有独立修改，先合并回来源项目，不自动覆盖 |
| BUSY | 其他更新正在执行，稍后再查，不删除正在使用的锁 |
| SOURCE_NOT_FOUND / REGISTER_REQUIRED / SOURCE_CHANGED | 核对项目路径；必要时明确 --register，不能继续宣称最新版 |

版本使用整套内容的 SHA256 指纹，而非文件时间；返回 revision、source、target、changed 和必要的 backup 路径。来源变化会更新新增/修改文件；来源删除的文件仅在它曾被本工具管理且本地没有独立修改时删除。安装目录中其他文件保留。更新前备份在安装端 `.skill-backups/`，配置、锁与备份均不应提交 Git。

`--check` 只比较、不写入。`--project-root` 可显式选择来源，也支持 CINEMATIC_PREVIZ_PROJECT 环境变量；不传时读取安装端注册路径。更换已注册路径时需要 --register，且仍不会覆盖后续本地冲突。

“最新”指本次成功检查的项目内容。脚本不会擅自拉取/推送 GitHub：要采用远端更新，先在来源克隆中正常 git pull（有本地修改时先处理合并），再调用 Skill。网络不可用不会被误报为远端已更新。进程崩溃可能留下锁；只有确认没有更新进程，并核对备份和安装文件后才人工处理锁。

## 初始提示词

```text
使用 $cinematic-previz。先按注册的项目路径执行自更新，成功后重新读取最新版 Skill。
检查 Updream MCP 的连接、版本和可用画布，只做只读初始化，不修改节点或提交生成。
后续需要写入时，为本聊天创建独立工作区并认领目标项目，在我的授权范围内执行并核对结果。
```

不同项目可以并行；同项目跨标签页仍需排他认领。未知结果先核对、不重试整批。角色库、上传、音频和专用首尾帧等参数只按实际能力使用，不能猜字段。导演制作时，继续区分 continue/reangle/cut/reset，以实际选中视频的真实尾帧交接。

## 开发与发布

本仓库是 Skill 的发布内容；开发来源也可保存在 Updream 项目的 `skills/cinematic-previz`。内容更新先修改已注册来源，再同步安装目录；不要同时把两个目录当成独立权威版本。调用前同步不等于自动发布 GitHub。

保留上游许可和素材来源。此仓库没有账号凭证、素材资产或付费服务；真实生成只在用户已授权范围内进行。
