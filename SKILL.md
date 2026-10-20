---
name: cinematic-previz
metadata:
  author: "星迹"
description: Use when creating or revising 漫剧、短剧、导演分镜、Blender 白模预演、首帧生图、AI 视频、镜头接力，或在 Updream 使用 MCP 浏览器插件操作节点、多聊天分工和初始化工作区；不用于单独建模或普通视频转码。
---

# 星迹的AIGC

作者：星迹。显示名为星迹的AIGC，技术调用名保留为 $cinematic-previz。把剧情编译成专业分镜、逐镜完整提示词和Codex生图白模首帧；实际制作再按能力完成生成、真实尾帧衔接与剪辑。中文沟通，保留用户原稿、明确范围与既有偏好。

## 每次调用前先检查同步

有命令能力时，先运行本次实际安装目录的脚本：

~~~text
python "<skill-dir>/scripts/sync_from_project.py"
~~~

只在status=current或updated时继续，重新读取返回的skill_file和本次需要的参考；同步脚本自身更新时再跑一次。冲突、来源缺失或BUSY须保留本地修改/活锁并报告具体失败，不能绕过。无注册来源的普通下载包使用standalone，不猜项目根、不自动联网或git pull/push。已注册来源失败不能降级绕过。无命令能力且无宿主强制前置要求时，可阅读文本做独立规划，明确未运行检查。完整细则见 [运行与制作约束](references/workflow.md#每次调用前确认独立模式或项目同步模式)。

## 树状分类与横向组合

[模块索引](module-index.json) 是分类、父子关系、章节选择和跨分支依赖的唯一配置；[使用说明](references/module-loading.md) 解释读取和回退。目录树分为：

~~~text
星迹的AIGC
├─共享原稿、操作边界与状态规则
├─导演：风格 / 分镜 / 运镜 → 16类方法 / 转场 → 6类方法 / 打光 / 表演
├─制作：首帧与三维预演 / 提示词 / 生成 / 接力 / 交付
├─平台：Updream工作区 / 上传 / 工具 / 维护
└─资料：完整示例 / 来源 / 许可
~~~

先按用户任务选分支，再按剧情选具体方法；同一任务可组合多个角度，读取器自动带上父层公共正文和跨分支依赖，稳定去重，不自动读入所有兄弟分支。模型负责叙事判断，代码负责取资料，不用关键词匹配替代导演选择。

~~~text
python "<skill-dir>/scripts/read_modules.py" tree
python "<skill-dir>/scripts/read_modules.py" read storyboard camera.rise-orbit
python "<skill-dir>/scripts/read_modules.py" read camera.orbit lighting
python "<skill-dir>/scripts/read_modules.py" read platform.upload
~~~

完整分镜选storyboard，完整影片制作选workflow，动作/风格/平台单项查询选相应节点。storyboard必须展开风格、摄影、打光、表演、首帧、完整提示词、连续性和交付检查；有具体运镜或转场时追加对应叶节点。不得用一个单项查询包冒充完整脚本。

读取器是Python标准库只读工具，不会执行选中的脚本、调用模型、提交付费生成或清空已读上下文。tree只输出目录；read返回正文、来源和指纹，--json可保留结构；--max-chars仅约束正文字符，超限报错而不截断。不能为了节省内容删除必需规则或交付项，必要时分阶段读取后合流。无Python时按索引人工读取core、所选节点、父层正文及requires依赖，依赖/章节错误要报告，不能称代码校验通过。

## 完整脚本的交付不可缩减

按 [专业分镜规范](references/director.md#默认交付专业分镜表) 保留六项视觉参数包、叙事摄影表、视觉美术表、对应镜号的首帧白模预演和逐镜完整提示词表；不砍栏目，不只给概要、JSON或链接。

逐镜依次完成并核对：剧情与情绪 → 构图/风格/色调/配色 → 主体表演 → 机位/运动/焦点/时间 → 光影 → 台词/声音 → 连续性与接点 → 白模词/正式首帧词/视频词/声音与负向约束，最后按同一镜号整合交付。每条提示词全文入表、独立可复制，不能写同上或未填变量。执行原词和新的修订规划分别留版本；细则见 [逐镜交付检查](references/workflow.md#逐镜交付逐项核对)。

默认每个逻辑镜头用内置生图生成单幅白模起幅，主角可用稳定身份色，实际审图后回填；身份色不改正式服装。用户明确仅文字/已有可复用图/实际无能力时标明缺项。仅更新技能不自动生成示范影片。首帧流程见 [previs.start](references/first-frame-previz.md)。

有剧情直接推导风格和情绪，不让用户选导演姓名。原文台词保留；continue原样使用选中前片真实出点帧，不重画、不重复动作；reangle用真实末态与新构图分工。大量必须读准且随画面生成的文字先校对中间关键帧，后期加字保留无字画面。静态图、结构校验、三维轨迹和实际音画分别验收，状态必须与真实文件/检查一致，详见必读core和delivery。

涉及付费生成先读budget并核实现价、人民币换算、元/生成秒及既有授权，默认预算1元/秒；不把预算当付款授权。平台操作读platform.updream及具体分支，沿用工作区认领与真实参数。实际能力、素材或前片缺失则准备独立部分并如实标记，不编造提交、工具或验收结果。核心旧规则及完整制作链保留在 [workflow.md](references/workflow.md)，原有工具与参考文件继续可用。
