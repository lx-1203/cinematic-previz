# 整合来源与适用边界

核对日期：2026-10-19。该 skill 是为当前用户整合编写的独立流程；不打包上游服务、原脚本或完整 skill，不要求安装整个上游仓库。

## DirectorSKILL

- 仓库：[wuwangzhang1216/DirectorSKILL](https://github.com/wuwangzhang1216/DirectorSKILL)
- 核对提交：`c65ae0d14457053efb1e354c7e7f7e120d97fad1`。
- [主 skill](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/SKILL.md)、[生产工作流](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/references/production-workflow.md)、[QC](https://github.com/wuwangzhang1216/DirectorSKILL/blob/c65ae0d14457053efb1e354c7e7f7e120d97fad1/assets/qc-checklist.md)。
- 借鉴：先确定镜头目的与调度，再准备关键帧和运动提示；生成前、单片段后、全片剪辑后分别检查。
- 调整：不采用其固定时长建议、评分阈值或导演风格目录作为普遍标准；按用户题材、实际模型和可用工具选择。

## Scenario 两种预演

- 仓库：[scenario-labs/skills](https://github.com/scenario-labs/skills)
- 核对提交：`ccc6c5c623a4f96423df0d157b8ef174f14edfd8`。
- [导演预演](https://github.com/scenario-labs/skills/blob/ccc6c5c623a4f96423df0d157b8ef174f14edfd8/skills/dcc/blender/scenario-blender-previs-storyboard/SKILL.md)：用粗场景、机位图和定时分镜判断信息与节奏。
- [生成引导白模](https://github.com/scenario-labs/skills/blob/ccc6c5c623a4f96423df0d157b8ef174f14edfd8/skills/dcc/blender/scenario-blender-blockout/SKILL.md)、[交接规则](https://github.com/scenario-labs/skills/blob/ccc6c5c623a4f96423df0d157b8ef174f14edfd8/skills/dcc/blender/scenario-blender-blockout/references/handoff.md)：把运动、位置、外观的参考职责分开，制作干净引导片并与结果并排核对。
- 调整：去除对 Scenario 插件、付费服务和固定 Blender 版本的强制依赖。多图风格板仅在合适的参考视频路线采用；不是所有首帧任务都必须做风格板。当前能力现场核实。

## 用户指定的衔接策略

需要换机位的剧情接点可从上一真实尾状态生成新角度首帧；超出单次生成时长的连续长镜头直接以真实尾帧续接。不是每节都换角度。该策略与版本指纹、动作状态和片段时间轴结合，是本 skill 的核心个性化部分，不宣称任何一种方式在所有镜头都最好。

上游 MIT 版权和许可全文保存在 [upstream-licenses.txt](upstream-licenses.txt)。本包的原创工具不含上游 Python 源码。

## 运镜与打光一手资料（2026-10-21）

- [M. David Mullen, ASC：Notes on Camera Movement](https://studentfilmmakers.com/notes-on-camera-movement-when-to-move-the-camera-and-why-by-m-david-mullen-asc/)：参考其从戏剧动机与剪辑需要判断何时运动的思考方式，不把个人焦距选择或具体影片镜头当成统一模板。
- [ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)：用于核对软硬光及主光、补光、分离与背景光的区分。没有复制手册图片、完整章节或特定灯具配方。
- 场次视觉递进、逐镜运动/光线交付字段、AI能力适配与验收规则为本技能原创设计；不承诺仅凭术语即可得到某种电影效果。
