---
name: cinematic-previz
metadata:
  author: "星迹"
  version: "0.6.0"
  plugin_version: "0.6.0"
description: Use when creating or revising 漫剧、短剧、导演分镜、Blender 白模预演、首帧生图、AI 视频、镜头接力、漫剧项目目录整理与回收恢复，或在 Updream、即梦使用 MCP 浏览器插件操作节点、多聊天分工和初始化工作区，或通过 LibTV 官方 Remote MCP 复用素材与整理画布；不用于单独建模或普通视频转码。
---

# 星迹的AIGC

作者：星迹。显示名为星迹的AIGC，技术调用名保留为 $cinematic-previz。先优化为传统文档剧本，经用户审核后制作Excel多列分镜、资产和首帧；含首帧的Excel获审核后，再按表内原词制作视频，最后用OpenCut剪辑与导出。中文沟通，保留用户原稿、明确范围与既有偏好。

当前本机技能内容版本为 **0.6.0**；[release.json](release.json) 中的 Updream MCP Bridge **0.6.0** 是历史配对声明，不是 GitHub 发布回执或完整 Bridge 源码证明。变化见 [更新记录](CHANGELOG.md)，SHA256 revision 用于核对具体内容；历史日期版本保留。维护更新后的远端备份另按 [维护更新收尾](references/maintenance-release.md) 验收。

## 每次调用前先检查同步

有命令能力时，先运行本次实际安装目录的脚本：

~~~text
python "<skill-dir>/scripts/sync_from_project.py"
~~~

只在status=current或updated时继续，重新读取返回的skill_file和本次需要的参考；同步脚本自身更新时再跑一次。冲突、来源缺失或BUSY须保留本地修改/活锁并报告具体失败，不能绕过。无注册来源的普通下载包使用standalone，不猜项目根、不自动联网或git pull/push。已注册来源失败不能降级绕过。无命令能力且无宿主强制前置要求时，可阅读文本做独立规划，明确未运行检查。完整细则见 [运行与制作约束](references/workflow.md#每次调用前确认独立模式或项目同步模式)。

普通调用的本机同步不触发推送；修改维护源码或回写经验后，必须按 [维护更新收尾与 GitHub 备份](references/maintenance-release.md) 执行。用户已有“每次更新上传 GitHub”授权时自动完成精确范围提交、非强推上传及远端 commit／文件核验，不重复索要同一权限，也不自行把“不发布”加入计划。没有相应授权不自行公开；缺 Git、权限、网络或存在分叉时标记 `backup_pending`，不能把本机 `current` 或 `remote_checked=false` 说成远端已备份。

## 树状分类与横向组合

[模块索引](module-index.json) 是分类、父子关系、章节选择和跨分支依赖的唯一配置；[使用说明](references/module-loading.md) 解释读取和回退。目录树分为：

~~~text
星迹的AIGC
├─共享原稿、操作边界与状态规则
├─导演：风格 / 分镜 / 运镜 → 16类方法 / 转场 → 6类方法 / 打光 / 表演
├─制作：人物双参考五视图 / 标准表情合集 / 强参考物品资产 / 首帧与三维预演 / 提示词 / 生成 / 执行检查 / 接力 / 交付 / 目录整理与回收
├─平台：Updream工作区 / 上传 / 工具 / 维护；即梦页面 / 画布 / 协作；LibTV官方Remote MCP / 素材复用
└─资料：完整示例 / 来源 / 许可
~~~

先按用户任务选分支，再按剧情选具体方法；同一任务可组合多个角度，读取器自动带上父层公共正文和跨分支依赖，稳定去重，不自动读入所有兄弟分支。模型负责叙事判断，代码负责取资料，不用关键词匹配替代导演选择。

~~~text
python "<skill-dir>/scripts/read_modules.py" tree
python "<skill-dir>/scripts/read_modules.py" read storyboard camera.rise-orbit
python "<skill-dir>/scripts/read_modules.py" read camera.orbit lighting
python "<skill-dir>/scripts/read_modules.py" read character-assets
python "<skill-dir>/scripts/read_modules.py" read expression-assets
python "<skill-dir>/scripts/read_modules.py" read prop-assets
python "<skill-dir>/scripts/read_modules.py" read previs.start
python "<skill-dir>/scripts/read_modules.py" read organization
python "<skill-dir>/scripts/read_modules.py" read platform.upload
python "<skill-dir>/scripts/read_modules.py" read platform.jimeng
python "<skill-dir>/scripts/read_modules.py" read platform.libtv
~~~

完整分镜选storyboard，完整影片制作选workflow，动作/风格/平台单项查询选相应节点。storyboard必须展开风格、摄影、打光、表演、首帧、完整提示词、连续性和交付检查；有具体运镜或转场时追加对应叶节点。不得用一个单项查询包冒充完整脚本。

仅制作或修订首帧也读previs.start，它自动带入人物阶段资产、表演、[标准表情合集](references/expression-assets.md)、[强参考物品](references/prop-assets.md)和[执行检查](references/execution-checks.md)。先逐镜核对剧本时期、年龄阶段、衣装及活动／身体状态，选用匹配人物资产；同人同阶段表情标准化为一张覆盖喜怒哀乐的合集，选用格位入镜；文字、书籍、地图等先有独立物品图并设计读者方向，再补齐、审图并真实附入生图工具；不能只写资产路径或沿用设定图的中性脸。调用前核对first_frame输入，调用后核对真实附件并审图；continue仍原样用真实出点帧。转场按[改版落实规则](references/transitions.md#转场改版与逐项落实)更新两侧素材、Excel和剪辑任务，交付按delivery检查逐项核对，再回放最终输出。机械检查不代替实际表情和转场验收，也不授予提交权限。

整理项目、分类素材、归档或回收恢复时选 `organization`（[目录整理与项目回收站](references/project-organization.md)），自动带入 `records`。按实际文件展示架构；以制作登记解析当前版本，保留活跃源路径与素材来源，区分浏览快照、历史版本和可恢复批次。仅整理不触发制作、生成或自动永久删除。

读取器是Python标准库只读工具，不会执行选中的脚本、调用模型、提交付费生成或清空已读上下文。tree只输出目录；read返回正文、来源和指纹，--json可保留结构；--max-chars仅约束正文字符，超限报错而不截断。不能为了节省内容删除必需规则或交付项，必要时分阶段读取后合流。无Python时按索引人工读取core、所选节点、父层正文及requires依赖，依赖/章节错误要报告，不能称代码校验通过。

## 制作顺序与提示词来源

执行[十步制作与审核流程](references/workflow.md#制作阶段与审核顺序)：文档剧本 → 用户审核 → Excel多列分镜 → 人物/场景/表情/物品资产逐镜映射 → 批量首帧嵌入Excel → 用户审核含图Excel → 平台上传素材 → 对应节点与连线 → 严格读取Excel视频提示词 → OpenCut剪辑、字幕、导出。两个审核关口必须有对应版本的用户通过证据；沿用已有通过和范围授权，不重复索要，也不越过尚未通过的关口。

Updream新建、上传或复用画布素材后，按[画布资产节点命名与验收](references/updream-mcp.md#画布资产节点命名与验收)整理并读回显示名称，再完成本批生成前核对；本地文件名规范不能代替画布命名。保留用户已有清楚的命名体系，只处理本次授权范围内的节点。

已有正式Excel视频词时，先读实际完整单元格，记录工作簿版本/指纹、工作表、单元格与镜号；不得跳过Excel从旧JSON、图片或记忆现写、重组、删减或追加视频词。用户要求改音色等内容时，先按授权更新Excel并留版本，再读取表内完整词执行。写入后逐字读回核对；能力缺口记待办，不改词迁就。详见[Excel原词执行](references/generation.md#视频提示词以已审核Excel为唯一执行来源)。

未明确要求时不自主生成规划尾帧；真实视频尾帧提取与生成规划尾帧分开。最终字幕默认宋体、白字黑边。仅更新本技能不启动当前项目的素材、视频或剪辑生产；项目已有“仅草稿/不提交”边界继续有效。

剧本拆句与发声生成节点严格遵守[完整句边界](references/workflow.md#剧本拆分的完整句边界)：以 `。？！` 等句末标点和完整句意为单位，一句一个发声单元；不能在逗号、顿号、分号、冒号或半句话处截断，也不能为凑时长用声桥拆句。**默认每个视频生成片段为 4–8 秒；用户或项目另行写明时长范围时以该明确范围为准。** 4–8 秒是常见硬限制，不得把多个视觉镜头合并成 10–30 秒长节点，也不得用完整句聚合或模型支持更长时长绕过。长完整句由独立旁白连续跨片段；超过 8 秒的逻辑镜头拆成连续片段，后续片段用真实尾帧接续。项目显式放宽上限时保留书面依据。句内画面变化留在逻辑镜头内，无对白动作镜按动作组织；长句超限保留原文并说明冲突。拆分后运行节点检查并人工审读；建立生成片段计划后运行 `python scripts/validate_duration_limits.py <plan.json>`，不把标点或时长自动检查通过当成语义和成片验收。

## 分镜阶段的完整交付不可缩减

按 [专业分镜规范](references/director.md#默认交付专业分镜表) 以核心主表作为单一当前交接入口：同镜号汇集必要分镜设计、完整当前视频词、实际选中首帧、人物/场景/表情/物品最终参考图与ID/版本/职责、可复用参考节点及依赖、真实平台ID或未创建状态、生成参数和审核/缺口。交给别人后须能取到素材、复制原词并重建流程，不能只给本机绝对路径或跨表索引。保留叙事摄影、视觉美术和完整提示词三类语义，附表存基线、完整原稿、资产来源/专业物品词、规划历史与实际执行证据；不硬定镜数、列数或表数。主表入出点与已知帧数合入A列“镜号／时间”，构图单列。当前词唯一维护，其他必要展示同步；待审核规划不能称最终可执行，真实历史调用不覆盖。

逐镜依次完成并核对：剧情与情绪 → 构图/风格/色调/配色 → 主体表演 → 机位/运动/焦点/时间 → 光影 → 台词/声音 → 连续性与接点 → 白模词/正式首帧词/视频词/声音与负向约束，最后按同一镜号整合交付。每条提示词全文入表、独立可复制，不能写同上或未填变量。执行原词和新的修订规划分别留版本；细则见 [逐镜交付检查](references/workflow.md#逐镜交付逐项核对)。

首帧在流程第5步按已选正式图或白模类型逐镜批量制作，实际审图并嵌入Excel；已有合格首帧直接复用，不为凑流程额外生成两套。白模主角可用稳定身份色，身份色不改正式服装。文档剧本审核前不先做分镜或生图；仅文字/已有可复用图/实际无能力时按实际范围交付。首帧流程见 [previs.start](references/first-frame-previz.md)。

白模与正式参考首帧都须按[首帧的互动、视线与场景表情](references/first-frame-previz.md#首帧的互动视线与场景表情)编译开镜表演并实际审图，不沿用人物资产的固定严肃脸；仅修改首帧时不扩展重做尾帧或全片。

核心主表逐镜分设**人物参考、场景参考、表情参考、物品参考**四栏，展示最终选图及职责，不能只在附表可见；原图须可从Excel导出或随包取得，缩略图与原图版本对应。凡承载专业知识的黑板、面板、书籍、图表、仪器与设备界面，先按[物品参考与专业内容稿](references/generation.md#物品参考与专业内容稿)核对知识与文字，保存独立完整的物品资产提示词并制作清楚的正视或展开参考；沿用用户指定的确认顺序和已认可版本。

新建、重绘或批量更新人物资产必须读 [character-assets](references/character-assets.md)：盘点全部出镜人物及年龄／年代阶段，按 person_id＋variant_id 核对图1唯一面部参考、图2唯一服装搭配参考，使用完整五视图提示词逐图审查并映射到镜头；已确认双参考及缺少阶段／不可见衣装的既有推演授权直接沿用，不新增逐图审批。未获授权的缺项不猜造身份或穿搭，同人现用阶段图按 [organization](references/project-organization.md#人物目录与阶段文件) 集中分类。年代、场地或原有标牌文字等常规缺口继续按[资产缺口自动补齐](references/generation.md#资产缺口自动补齐)查史料并复核，不擅自改写镜头或改成背影。

有剧情直接推导风格和情绪，不让用户选导演姓名。原文台词保留；continue原样使用选中前片真实出点帧，不重画、不重复动作；reangle用真实末态与新构图分工。大量必须读准且随画面生成的文字先校对中间关键帧，后期加字保留无字画面。静态图、结构校验、三维轨迹和实际音画分别验收，状态必须与真实文件/检查一致，详见必读core和delivery。

多人镜头按[多人调度与危机反应](references/performance-compiler.md#多人调度与危机反应)逐人/逐组错开姿态、朝向、视线、手部与动作阶段；空袭等危机用可见避险反应传达压力，实际审图排除复制动作与平静摆拍，保留共同路线和人物连续性。

涉及付费生成先读budget并核实现价、人民币换算、元/生成秒及既有授权，默认预算1元/秒；不把预算当付款授权。Updream操作读platform.updream及具体分支；即梦操作读platform.jimeng，使用其字符串节点ID和真实参数，不套用Updream数值节点接口。LibTV操作读platform.libtv（[官方接入与素材复用](references/libtv-mcp.md)），复用宿主已授权的官方Remote MCP，按本次schema定位项目、交接右栏真实画布并核验素材／节点；仅建节点不自动生成，视频草稿须由实时能力明确支持。本次为技能路由集成，不表示浏览器Bridge源码或安装包已集成LibTV。仅开发插件或更新技能时，不认领或操作制作画布，也不安排生成。实际能力、素材或前片缺失则准备独立部分并如实标记，不编造提交、工具或验收结果。核心旧规则及完整制作链保留在 [workflow.md](references/workflow.md)，原有工具与参考文件继续可用。

## 插件缺口反馈

缺少工具、能力未覆盖或可复现调用失败时，读取 `platform.feedback`（[GitHub反馈流程](references/github-feedback.md)）：本地记录、脱敏、查重，在用户明确授权下提交至公开反馈仓库；没有GitHub连接时交付报告与提交链接。安装或使用技能本身不代表同意公开上报；不上传密钥、私有素材或整份日志。用户要求全程只用插件时，缺口记入待办，不以界面操作绕过。
