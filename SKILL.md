---
name: cinematic-previz
metadata:
  author: "星迹"
  version: "0.6.0"
  plugin_version: "0.6.0"
description: Use when creating or revising 漫剧、短剧、导演分镜、Blender 白模预演、首帧生图、AI 视频、镜头接力、漫剧项目目录整理与回收恢复，或在 Updream、即梦使用 MCP 浏览器插件操作节点、多聊天分工和初始化工作区，或通过 LibTV 官方 Remote MCP 复用素材与整理画布；不用于单独建模或普通视频转码。
---

# 星迹的AIGC

Excel默认采用“逐镜脚本”主表＋“提示词指导”分表：六项设计指导只放分表，不在主表重复铺列；完整视频词、首帧及四类参考留在主表。默认不增加“来源位置”等定位列。栏目与导出校验见[分镜交付](references/director.md#默认交付专业分镜表)。视频正文必须按[分层格式及交付检查](references/prompts.md#提示词正文交付检查)展开，导出后运行布局＋正文联合校验；待审核稿同样检查，不能只查表头或以“尚未定稿”解释格式缺失。

作者：星迹。稳定调用名 `$cinematic-previz`。根据剧情完成导演设计、资产与首帧、视频接力和剪辑；只执行用户当前要求的范围。内容版本 **0.6.0**，配对声明不代表完整Bridge源码或插件已发布，见 [发布说明](references/maintenance-release.md)。

## 每次调用前检查同步

```text
python "<实际skill目录>/scripts/sync_from_project.py"
```

只在 `status=current/updated` 后继续，重新读取返回的skill_file和本次所需参考；同步器自身更新后再运行一次。冲突、BUSY、来源缺失或失败时保留本地改动和活锁并报告，不降级绕过。独立包不要求注册来源；无命令能力时的适用条件见 [运行规则](references/workflow.md#每次调用前确认独立模式或项目同步模式)。本机同步不证明远端最新。

## 范围与关键边界

每次加载必读 [共享边界](references/core.md)。新项目先交文档剧本并取得用户通过，再做Excel分镜、资产和首帧；含图Excel通过后才进视频制作，最终使用OpenCut剪辑导出。沿用已审同版和现有范围，不为查询或维护任务启动制作。完整顺序只在 [stages](references/workflow.md#制作阶段与审核顺序) 维护。

执行词只取已审核Excel，获授权改词先改表再读取；`continue`原样用实际出点尾帧；未要求不生成规划尾帧。生成时长与完整句、声音、预算分别按下方正式来源，不从示例猜默认值。缺能力、未执行和未验收如实标记。

## 按任务读取

分类、父子关系和跨分支依赖以 [module-index.json](module-index.json) 为唯一配置。运行读取器可自动带入core和必要依赖，不自动展开所有兄弟方法或所有平台。

```text
python "<skill-dir>/scripts/read_modules.py" tree
python "<skill-dir>/scripts/read_modules.py" read <模块ID> [其他模块ID]
```

| 当前任务 | 入口模块 |
| --- | --- |
| 单项风格、表演、打光、声音 | style / performance / lighting / sound |
| 一种运镜或转场 | camera.<方法> / transitions.<方法>；先tree查ID，按剧情选叶节点 |
| 完整分镜 | storyboard；具体运镜和转场再追加所选叶节点 |
| 人物、表情、物品资产 | character-assets / expression-assets / prop-assets |
| 首帧或三维预演 | previs.start / previs.3d |
| 提示词、时长、完整句 | prompts / timing |
| 实际生成与接力 | generation / handoff；按阶段选平台 |
| 全片制作、记录、整理、交付检查 | workflow / records / organization / delivery |
| 平台操作 | platform.updream及对应子模块 / platform.jimeng / platform.libtv |
| 技能维护或故障反馈 | runtime；[维护收尾](references/maintenance-release.md) / platform.feedback |

完整分镜保留全部专业分支及独立可复制的逐镜完整词，不以单项查询输出冒充整套交付。模块加载只减少无关阅读，不减少用户要求的交付。规则归属、依赖与兼容入口见 [读取说明](references/module-loading.md#公共规则的正式来源)。

## 维护收尾

修改注册来源，验证后同步安装并读回。沿用已有GitHub备份授权完成精确提交、非强推上传和远端文件核验，按 [维护指南](references/maintenance-release.md) 分别报告本机与远端状态；无发布授权不自行公开，阻塞记backup_pending。源码缺失的Bridge不冒称完整插件。缺工具时按 [反馈流程](references/github-feedback.md) 保留脱敏记录；公开上报须有对应授权。
