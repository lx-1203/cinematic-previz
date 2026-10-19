# 项目记录与可执行示例

## 最小项目结构

在用户指定项目目录内保存；未指定时新建任务目录，保留用户现有文件。文件采用 `SH010_SG01_v01` 这类稳定 ID 和版本。别用“最新文件”自动替代已选版本。

```text
project/
  production.json
  direction/       导演分镜、空间与角色设定
  blender/         可编辑工程、场景脚本和机位图
  previs/          导演预演
  guides/          无标注的生成引导片
  frames/          选中首帧、关键帧和固定参考
  clips/           各生成片段及明确的 selected 版本
  handoffs/        真实尾帧、提取凭据、交接检查
  edit/            逻辑镜头合成、声音与最终视频
```

`production.json` 不是第三方 API 请求体。只创建当前任务需要的记录，不为每个小任务批量生成空文件。

## 记录字段

项目：标题、画幅、帧率、时长、原始设定引用、工具与实际能力、用户已授权的范围/预算。

逻辑镜头：scene/section/shot ID、叙事任务、信息变化、构图与运动、动作起止、全局时长、角色/道具/空间约束、片段 ID 列表。

生成片段：所属镜头、segment ID、逻辑镜头内时间区间、首帧、引导片、生成路线与实际模型、提示文件、任务状态、视频版本与指纹、实际保留范围、选中版本、检查结果。

交接：源 segment/版本/指纹、真实尾帧和提取凭据、`continue/reangle/cut/reset`、状态清单、新机位构图来源、目标首帧与视频、依赖项、检查状态。

所有帧编号说明是 0-based 还是 Blender 1-based，禁止混用。脚本提取工具采用 **0-based 解码显示顺序**；Blender 时间轴通常从 1 起。VFR 源视频的时长/帧号不能只用平均 FPS 换算；统一时间基准时先转码并记录转换来源。

状态机：

`planned → ready → submitted → generated → reviewed → selected`

缺能力/素材为 `blocked`；被改版来源影响为 `stale`。不要通过改标签把缺失或未查看的文件标为通过。

## 示例：先长镜头续接，再切机位

这是**规划示例**，没有附带真实图片或视频。假设现场核实目标工具最多 6 秒且支持首帧输入，设计 12 秒长镜头，再切一个 3 秒特写。真实任务根据当前模型重新核实时长。

场景：女子右手持钥匙靠近门，男友在她后方走廊。门向室内开启，门框、锁和两人关系在白模中固定。

| ID | 全局镜头时间 | 任务 | 结束状态 | 接下一段 |
|---|---|---|---|---|
| SH010/SG01 | 0–6 秒 | 同一跟拍镜头，女子走近门 | 到门前，右手抬起但钥匙未接触锁 | continue |
| SH010/SG02 | 6–12 秒 | 保持跟拍机位和运动趋势，完成插钥匙 | 钥匙插入、尚未转动，门仍关闭 | reangle |
| SH020/SG01 | 0–3 秒 | 切门外锁具特写，看清开锁 | 右手转动钥匙，开锁完成 | cut 或按后续剧情选择 |

执行顺序：

1. 完成导演分镜，安排空间和动作；在 Blender 同一 SH010 曲线上规划 0–12 秒。
2. 生成 SH010/SG01，选中真实视频和剪辑范围后提取尾帧，记录检查。
3. 以该 PNG **原样**作为 SH010/SG02 首帧；接着抬手接近并插入钥匙，不重新走到门前。引导片使用 SH010 曲线 6–12 秒。
4. 提取 SG02 的实际尾帧，确认钥匙、手别、门和男友位置。若实际未插入，先处理该差异。
5. 把此状态冻结在 Blender，摄影机移到**门外**锁具特写，检查朝向和遮挡。首帧保持“插入、未转动”。
6. 生图时实际附上 SG02 尾帧、新机位白模、人物/手部服装及道具参考；生成 SH020 首帧，检查通过后生成转动钥匙的镜头。
7. SH010 两段拼成同一长镜头，检查接点运动速度；SH010→SH020 是有意切机位，检查动作接点和声音。

门内反打是另一种设计：关门时门板会遮挡人物，可拍门内锁具/门板并以画外声音传递动作，或等门打开后再看到人物。不要把门外图简单翻转成门内视角。

## 项目 JSON 示例

```json
{
  "schema_version": 1,
  "title": "走廊开锁",
  "status": "planned",
  "format": {"aspect": "16:9", "fps": 24},
  "capabilities": {"verified": false, "image_to_video": null, "max_seconds": null, "reference_video": null},
  "shots": [
    {"shot_id": "SH010", "scene_id": "SC01", "section_id": "SEC01", "duration_seconds": 12, "segments": ["SG01", "SG02"], "purpose": "连续跟随至关键线索"},
    {"shot_id": "SH020", "scene_id": "SC01", "section_id": "SEC02", "duration_seconds": 3, "segments": ["SG01"], "purpose": "确认钥匙转动与开锁结果"}
  ],
  "handoffs": [
    {"from": "SH010/SG01", "to": "SH010/SG02", "mode": "continue", "source_video": null, "tail_receipt": null, "next_start": null, "status": "planned"},
    {"from": "SH010/SG02", "to": "SH020/SG01", "mode": "reangle", "source_video": null, "tail_receipt": null, "next_start": null, "status": "planned"}
  ]
}
```

null 表示尚未取得/验证，不是允许把缺项当作 ready。为实际制作补充上一节字段；不要把示例的假设能力写成现场已验证能力。
