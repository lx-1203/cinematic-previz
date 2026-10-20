# 星迹的AIGC

作者：**星迹**。技术调用名：**cinematic-previz**。

把专业分镜、逐镜首帧白模生图、按需Blender预演、正式首帧、真实尾帧接力、视频生成与剪辑连起来。镜头变化按叙事选择；连续长镜头超过单次生成时长时，直接用真实尾帧同机位续接。

## 版本与更新记录

当前发布版本：**v2026.10.21.7**。功能变化见 [更新记录](CHANGELOG.md)；Git 标签固定对应发布提交，历史版本可通过标签取得。同步脚本的 SHA256 revision 用于核对具体文件内容，不替代发布版本号。

## 普通用户：下载即可安装，不需要开发者项目

如果使用附带浏览器插件的技能整合包（旧版文件名 `AI漫剧-skill.zip`），解压后先读顶层 `安装说明.md`：顶层 `cinematic-previz` 是技能，`Updream-Node-Helper/extension` 是 Chrome / Edge 扩展，配套 MCP 服务也在该插件目录内。两部分分别安装；浏览器登录和本机配对由使用者完成。

1. 下载并解压技能包，找到直接包含 `SKILL.md` 的文件夹。
2. 将这个文件夹命名为 `cinematic-previz`，放进当前宿主的技能目录。Codex 使用配置的 `CODEX_HOME/skills`，未设置时使用用户主目录下的 `.codex/skills`；其他宿主按其自身的技能安装方式使用。
3. 确认结构是 `skills/cinematic-previz/SKILL.md`，而不是多嵌一层下载目录。更新已有技能前先备份并处理自己的改动，不覆盖其他技能。
4. 让宿主重新发现技能，或在新聊天调用：

```text
使用 $cinematic-previz（星迹的AIGC），根据这个剧本设计镜头和制作方案。
```

“星迹的AIGC”是界面显示名称；`$cinematic-previz` 是稳定调用标识。也可用自然语言说“使用星迹的AIGC”。只下载 ZIP、尚未解压安装时，宿主无法发现里面的技能。支持 Agent Skills 或可读取 Markdown 的宿主可以使用核心流程；具体调用界面由宿主提供。

普通用户**不需要** `.skill-source.json`、作者电脑目录、Git 仓库、Updream 账号或 API key 才能做导演分镜与提示词。基础流程不依赖某个视频平台；安装 skill 不会自动安装 Blender、浏览器扩展或生成模型。

## 运行能力按功能准备

| 使用内容 | 需要什么 |
| --- | --- |
| 文字分镜、镜头设计、提示词与接力规划 | 能加载技能或读取Markdown的AI宿主 |
| 逐镜首帧白模预演 | 宿主内置生图能力，Codex优先使用image_gen |
| 本地模式检查、可选项目同步 | Python 3.11+，只用标准库 |
| 精确尾帧提取 | Python 和 FFmpeg，可显式指定现有 FFmpeg 路径 |
| 白模实际渲染 | 本机 Blender 或可用桥接 |
| 实际生图/视频 | 当前宿主已提供的相应能力；平台和账号由使用者选择 |
| Updream 节点操作 | 单独安装并连接 Updream MCP Bridge，仅选择此平台时需要 |

缺少某项能力时明确标记该阶段未执行，继续能独立完成的部分；不要把规划文件称为已生成影片。若用户的 AGENTS 明确要求每次先执行同步检查，优先遵循该要求，失败不能跳过。

## 独立模式与可选项目同步

有命令能力时，可在任何工作目录运行实际安装位置的脚本：

```text
python "<实际技能目录>/scripts/sync_from_project.py"
```

| 条件/返回值 | 意义 |
| --- | --- |
| 没有注册文件，也未显式指定来源；current + standalone | 当前本地包可以独立使用，不写文件、不联网；revision 只是此包内容指纹，不表示远端最新 |
| 已注册来源；current + project | 安装内容与本次成功检查的来源项目一致 |
| updated + project | 已同步；重新读取返回的 skill_file；若脚本自身更新，再运行一次 |
| update_available | 只比较模式发现更新，尚未应用 |
| LOCAL_CONFLICT / BUSY / 来源丢失 / 配置损坏 | 报告具体错误，保留本地修改和活锁；已经注册的用户不会自动降级绕过 |

### 维护者可选：从保留的源码目录更新

需要保留来源目录；同步目标必须与来源分开。来源既可以是独立技能根，也可以是大项目根下的 `skills/cinematic-previz`。

```text
python "<来源技能目录>/scripts/sync_from_project.py" --project-root "<保留的来源项目目录>" --target "<技能安装目录>/cinematic-previz" --register
```

注册使用真实路径，私有 `.skill-source.json`、备份和锁只留在安装端，不进入下载包。`--project-root` 或 `CINEMATIC_PREVIZ_PROJECT` 是显式来源选择；不传则读取已有注册。更换来源需要显式注册，已有冲突仍要先处理。不能自动把当前工作目录当作开发者项目。

版本用 SHA256 内容指纹；本地独立修改触发冲突保护，更新先备份到 `.skill-backups/`。`--check` 只比较，不写文件。脚本不会自动 git pull/push；来源目录内容也不等于远端最新。采用远端更新时先正常拉取合并，再同步。确认没有活跃更新进程之前不能移除更新锁。

## 内容入口

| 入口 | 内容 |
| --- | --- |
| [SKILL.md](SKILL.md) | 核心流程、模式与能力选择 |
| [视觉风格](references/visual-style.md) | 从剧情推导风格与情绪；构图、色调、配色、材质及六项参数包 |
| [导演设计](references/director.md) | 专业分镜、逐镜完整提示词表、景别、机位、运镜和剪辑理由 |
| [表演提示词编译器](references/performance-compiler.md) | 逐拍表演、语音、正负向约束、结构化JSON与本地校验器 |
| [逐镜首帧白模](references/first-frame-previz.md) | Codex内置生图、角色身份色、起幅审图与镜号关联 |
| [完整分镜示例](references/storyboard-example.md) | 同镜号的叙事、视觉、预演与逐镜完整提示词 |
| [Blender 双预演](references/blender.md) | 导演预演与模型运动引导片 |
| [尾帧接力](references/frame-handoff.md) | 换机位、长镜头续接、实际剪辑出点 |
| [生成适配](references/generation.md) | 图片职责与目标工具能力 |
| [Updream 插件](references/updream-mcp.md) | 选用该平台时再读，接口以实际连接为准 |
| [初始提示词](references/updream-prompts.md) | 节点任务和跨聊天协作 |
| [来源和许可](references/sources.md) | 上游来源与保留的许可 |

有付费生成需求时遵循用户实际授权范围。源代码与流程公开不表示底层生成服务免费，也不包含任何人的登录态、素材或凭证。
