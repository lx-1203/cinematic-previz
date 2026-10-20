# 树状模块读取与专业交付

分类像树：一个节点只有一个parent，根为aigc。执行依赖另用requires连接不同枝条，保持无环；分类归属和实际工作先后分开。新增类型通常只需在既有分支加叶节点及来源，不能复制一份公共规则。

## 使用现成代码

~~~text
python "<skill-dir>/scripts/read_modules.py" tree
python "<skill-dir>/scripts/read_modules.py" tree camera --json
python "<skill-dir>/scripts/read_modules.py" read camera.orbit lighting --json
python "<skill-dir>/scripts/read_modules.py" read storyboard camera.rise-orbit --json
python "<skill-dir>/scripts/read_modules.py" check --json
~~~

所有路径由脚本自身安装位置解析，不依赖作者电脑、当前工作目录、网络或第三方Python库。默认只读；不会执行模块内命令或调用生成服务。首次同步仍按SKILL前置要求执行，读取器不替代同步器。

- tree返回分支/叶节点名称和关系，不向模型展开规则正文。代码为验证目录可能在本地读取来源，模型上下文只接收实际返回内容。
- read接受一个或多个可读节点。先带上required共享规则，再按parent和requires依赖返回正文；相同节点只返回一次，兄弟分支不会自动展开。无正文分类只用于导航，直接read会列出可选children。
- check核对整个索引、树/依赖关系、文件和精确章节；status=valid只证明索引可读。read的status=loaded不代表脚本、图片、表演或视频验收通过。
- --max-chars限制返回的规则正文字符总数，不含来源等元数据，不是token预算；超限时退出2且无半份正文。应分阶段读取必要模块，不截断必需规则，更不能删减最终脚本。
- 缺ID、重ID、父链/依赖循环、越界/缺文件、标题消失或同名标题歧义均报错，不能默默选第一处或使用旧缓存。每次重新读取，结果带目录SHA256和每个源文件SHA256；它们只证明来源版本，不证明内容正确。

## 单项查询与完整交付是不同读取范围

查一种运镜可读camera对应叶节点并组合lighting/performance/style；完整脚本必须读storyboard，它自动包含全部专业交付分支。具体运镜方法由剧情决定后追加，不能只读摄影公共规则就假设已加载16种方法。完整制作使用workflow并按阶段补充具体平台和文字关键帧等分支，禁止按分类树把所有平台和全部示例一次性灌入。

完整脚本继续交付 [director.md](director.md) 的全部表格，逐镜过 [workflow.md的全维度检查](workflow.md#逐镜交付逐项核对)。分层按需减少的是当前不相关的参考，所有最终设计和提示词仍需展开。多阶段读取所得结果在同镜号、同版本下合流，不以零散模块输出代替完整脚本。

只有文字或示例模板的检查无法证明实际图片或运动通过。缺图、未知模型/资产、待上游真实尾帧、不适用音频等分别说明，保持已执行原词和规划版本，不能用“专业级”字样代替证据。

## 索引维护契约

module-index.json的version为格式版本1；root为唯一根节点ID；required为每次read都携带且有正文的共享节点。nodes按稳定展示顺序保存id、title、parent，可选requires和source。source.path为技能包内相对路径，source.sections可选、必须是源文件中唯一出现的完整ATX标题行，例如“## M03｜360°环绕”；不填sections才返回整个文件。

章节包含其子标题内容，截止下一个同级或更高级标题，代码围栏中的伪标题不参与定位；不要用行号当稳定接口。保持现有来源单一，不在索引写入正文副本。变更后运行check及scripts/test_read_modules.py，并检查受影响实际读取组合。无Python时按此相同依赖关系人工读取并明确未运行自动校验。
