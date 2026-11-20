---
layout: post
title: "声音驱动机器人文献调研"
date: 2026-11-20
author: Keith
categories: research
tags: [声音感知, Audio-VLA, VSLA, 世界模型, 多模态数据集, 文献调研]
toc: true
excerpt: "按声音驱动的动作策略、声音世界模型、声音具身数据集与评测三大类，整理十四篇代表工作，介绍问题、亮点、主框架与适用边界。"
---

声音可以补充视觉难以判断的接触状态，也能作为环境事件的触发信号，帮助机器人决定做什么、何时行动。本文围绕声音作为机器人观测、交互反馈与预测目标，采用以下三大类组织文献，重点关注环境声与接触声；语音仅在与情境决策有关时纳入。

| 三大类 | 核心问题 | 代表工作 |
| --- | --- | --- |
| 声音驱动的动作策略（含 Audio-VLA） | 听到声音后，如何选择、调整或触发动作？ | ManiWAV、Hearing Touch、Audio-VLA、HEAR、ListenVLA、OmniVLA、RoboOmni、MultiGen；SonicSense 提供主动感知支撑 |
| 声音世界模型 | 接下来会听到什么？执行动作后，视听环境如何变化？ | Learning Robot Manipulation from Audio World Models、Audio-Visual World Models |
| 声音具身数据集与评测 | 用什么数据训练，如何验证策略确实利用了声音？ | RH20T、STMM-12K / Habitat-Echo、SoundSpaces 2.0，以及各方法的配套数据与基准 |

分类依据是工作在研究中的主要用途，可以交叉归属。例如 HEAR 训练时预测未来声音，但部署时由策略直接执行，因此放在第一类；STMM 同时提出策略和基准，在第三类集中介绍。本文共整理十四篇工作，以 2023 年以来的研究为主，并保留 SoundSpaces 2.0 作为声场仿真的基础平台。年份按首次公开时间标注，具体阅读版本见各条目。

## 一、声音驱动的动作策略（含 Audio-VLA）

这一类主要把声音作为输入或反馈，用于接触状态判断、目标选择、动作时机和任务意图推断。既包括直接输出动作的策略，也包括服务于操作的主动声学感知方法。

### ManiWAV: Learning Robot Manipulation from In-the-Wild Audio-Visual Data（2024）

**解决的问题：** 视觉难以完整反映擦拭、翻动物体等操作中的接触状态，而传统机器人遥操作又限制了带声音示范的采集范围。

**亮点：** 在 UMI 手持设备中加入接触麦克风，让人类直接在不同环境中采集声音与动作示范，再迁移到机器人执行。论文验证了擦拭、翻贝果、倒出物体和魔术贴捆线等任务，提供了接触音频参与操作学习的完整方案。

**主框架：** 手持设备同步采集图像、接触声音与操作轨迹 → 视觉编码器和音频编码器提取特征 → 多模态融合 → 扩散策略生成动作序列 → 机器人执行并根据新观测滚动更新。

[论文][maniwav] · [项目][maniwav-project] · [代码与数据][maniwav-code]。依据 v2 的方法与实验。

### Hearing Touch: Audio-Visual Pretraining for Contact-Rich Manipulation（2024）

**解决的问题：** 接触丰富的操作需要细致反馈，但机器人接触音频示范有限，直接从少量数据学习声音表征较难。

**亮点：** 将接触麦克风记录的振动作为触觉线索，利用互联网音视频预训练的声音表征辅助真实机器人操作；验证翻贝果、舀取与拉拉链等任务。适合研究“少量机器人示范如何利用已有声音表征”。

**主框架：** 接触音频 → 预训练音频编码器，图像 → R3M 视觉编码器 → 自注意力融合 → 行为克隆策略输出动作块 → 根据新观测继续操作。

**适用边界：** 主要面向能产生有效振动的接触过程；论文讨论了机器人自身振动、弱动态操作和软物体声学信号不足等限制。

[论文][hearing-touch] · [项目][hearing-touch-project]。依据 v1 §III–IV、VI。

### SonicSense: Object Perception from In-Hand Acoustic Vibration（2024）

**解决的问题：** 被遮挡的内部状态、物体材料和局部形状难以仅凭外观判断，需要机器人主动交互来获取信息。

**亮点：** 利用手内交互产生的声学振动感知物体，研究容器内部状态、异质材料、三维形状重建与重识别，并在 83 个真实物体上评估。提供了“主动制造声音，再推断物理属性”的代表路线。

**主框架：** 启发式探索策略选择交互 → 传感器记录声学振动 → 学习模型融合交互中的观测 → 估计物体属性与结构。

**适用边界：** 这是主动声学感知系统，不能直接视为通用 VLA 或端到端学习的操作策略。

[论文][sonicsense] · [项目][sonicsense-project]。依据 v2 摘要与官方项目说明。

### Audio-VLA: Adding Contact Audio Perception to Vision-Language-Action Model for Robotic Manipulation（2025）

**解决的问题：** VLA 主要依赖视觉与语言，对碰撞、接触变化和操作完成过程的反馈感知不足，容易遗漏图像中不明显的动态信息。

**亮点：** 将接触声音直接引入 VLA，使动作决策能够使用交互过程中的声学反馈；同时在 LIBERO、RLBench 中增加碰撞相关声音，并提出 Task Completion Rate（TCR）评价过程完成情况。

**主框架：** 图像经 DINOv2、SigLIP 编码，声音经 AudioCLIP 编码 → 多模态投影对齐 → 与语言共同输入 Llama2 主干 → 通过 LoRA 微调学习动作输出 → 执行后持续接收视觉与声音反馈。

[论文][audio-vla]。依据 v1 §III–IV。

### Towards the Vision-Sound-Language-Action Paradigm: The HEAR Framework for Sound-Centric Manipulation（2026）

**解决的问题：** 提示音、碰撞声等短促信号可能在动作块执行期间出现并消失，机器人下一次更新策略时已经无法听到，导致漏响应或动作时机错误。

**亮点：** 显式研究动作执行间隔中的声音遗漏，将声音记忆、时间对齐和动作生成结合。配套 OpenX-Sound 用于音频增强预训练，HEAR-Bench 检查机器人是否在相关声音发生后才正确行动。

**主框架：** 视觉、流式声音、语言与本体状态输入 → Historizer 持续保存声音事件 → Envisioner 推理任务与阶段 → Realizer 通过流匹配生成动作块。训练时增加 Advancer 预测近未来声音 token，部署时移除该预测模块。

[论文][hear] · [项目][hear-project] · [代码][hear-code] · [OpenX-Sound][openx-sound]。依据 v2 §3–6；OpenX-Sound 的声音为合成增强。

### Listen Before Act: Audio-Conditioned Robot Manipulation with ListenVLA（2026）

**解决的问题：** 给 VLA 加入音频输入后，模型仍可能只依赖视觉或固定动作模式，缺少对声音变化与动作变化之间关系的明确学习。

**亮点：** 引入声音—动作绑定目标，在视觉、指令与机器人状态匹配的条件下，监督不同声音对应的动作差异。任务覆盖发声目标选择、延迟闹钟，以及先摇晃盒子或触发蜂鸣器再判断的主动感知。

**主框架：** 历史声音 → 语义声音特征与波形声学线索 → 音频 token 和特征调制接入 GR00T N1.7 → 结合视觉、语言与本体状态生成连续动作。训练联合使用动作监督与声音—动作绑定目标，并通过音频交换实验检查声音是否影响动作。

[论文][listenvla]。依据 v1 §III–IV；配套 LIBERO-Audio 包含八项任务、960 条示范。

### OmniVLA: Physically-Grounded Multimodal VLA with Unified Multi-Sensor Perception for Robotic Manipulation（2025）

**解决的问题：** RGB 预训练 VLA 难以直接解释麦克风阵列、红外和毫米波等异构传感器信息，额外模态的机器人数据又较少。

**亮点：** 提出 sensor-masked image，将传感器信息空间对齐并叠加到 RGB 的目标区域，复用预训练视觉编码器。声音实验利用麦克风阵列定位被衣物遮住的响铃手机，再移开遮挡物，提供了声音经空间表征进入 VLA 的路线。

**主框架：** 麦克风阵列信号 → 波束成形得到方位热图 → 与 RGB 标定对齐，结合 VLM 提示和 Grounded SAM 2 目标掩码生成传感器图像 → 冻结视觉编码器与各传感器投影层 → 默认以 SmolVLA 为基础的模型输出动作块。

**适用边界：** 声音分支主要保留声源空间线索；论文中的声音操作集中于遮挡声源定位与移除遮挡，尚不能据此推断其具备细粒度接触音色或广泛声音事件理解能力。

[论文][omnivla] · [代码][omnivla-code]。首次公开于 2025 年，依据 2026 年修订的 v3 §III–IV。

### RoboOmni: Proactive Robot Manipulation in Omni-modal Context（2025）

**解决的问题：** 机器人通常等待明确指令，难以根据多人对话、环境声音和视觉上下文推断用户当前需要的操作。

**亮点：** 将声音与视觉用于情境意图理解，连接主动任务推断、交互确认和动作执行；构建约 14 万条 episode 的 OmniAction，为声音上下文到动作提供训练资源。其音频主要由语音合成、事件声插入与背景混音构成。

**主框架：** Perceiver 编码视觉、语音和环境声音 → Thinker 推断意图与任务 → Talker 生成语音回应或确认，Executor 输出机器人动作 → 根据后续交互更新任务与执行。

[论文][roboomni] · [代码][roboomni-code] · [OmniAction 数据][omniaction]。依据 v3 §3–4 与实验。

### The Sound of Simulation: Learning Multimodal Sim-to-Real Robot Policies with Generative Audio（MultiGen，2025，CoRL）

**解决的问题：** 物理仿真能生成大量操作轨迹，但难以提供逼真的交互声音，限制了视听策略从仿真迁移到真实环境。

**亮点：** 用生成音频补足物理仿真，在倒液体任务中训练视听操作策略并迁移至真实机器人，测试未见容器与液体。其价值是降低真实机器人视听示范的采集需求。

**主框架：** 真实人类倒液体视频用于微调 MMAudio，并借助 RGB 与语义掩码减小视觉域差异 → RoboVerse 生成物理仿真轨迹 → 生成同步声音 → 视听扩散策略学习 → 真实机器人执行。

**适用边界：** 不使用真实机器人训练数据，但声音生成器使用了真实人类视频，不能表述为“无需任何真实数据”。研究集中于倒液体；生成音轨用于策略训练，本文将其归入动作策略，未将其视为动作条件的在线世界模型。

[论文][multigen] · [项目][multigen-project]。依据 v2 §3–4 与 arXiv 的 CoRL 2025 标注。

## 二、声音世界模型

这一类把未来声音或未来视听观测作为显式预测目标，再用于机器人决策。阅读时应区分：预测是否以候选动作为条件、是否支持多步推演，以及预测结果是否真正参与部署决策。这里集中保留两篇直接相关的工作。

### Learning Robot Manipulation from Audio World Models（2025）

**解决的问题：** 只利用当前声音难以提前判断操作过程的发展，例如根据注水声音变化决定何时停止，需要对未来声音进行预测。

**亮点：** 将声音未来预测接入动作策略，让机器人利用预测结果提前准备或停止动作。论文在真实机器人注水和仿真钢琴任务中验证；声音预测以历史音频为条件，主要用于特定过程的前瞻。

**主框架：** 历史音频转换为频谱 → 编码到声音潜空间 → 流匹配模型生成未来声音 → 当前图像、当前声音与预测声音共同输入动作策略 → 输出机器人控制量。声音模型与策略分阶段训练。

**适用边界：** 模型以历史音频为条件，没有显式输入候选动作；适合声音过程前瞻，不能直接当作可比较任意候选动作后果的反事实动力学模型。策略训练使用真实未来音频，测试时再接入模型预测，需要注意二者的分布差异。

[论文][audio-wm]。依据 v1 §2–3。

### Audio-Visual World Models: Learning Physically Grounded Multisensory Dynamics（2025）

**解决的问题：** 视觉世界模型缺少对声音变化的预测，难以同时描述机器人移动后看到什么、听到什么，以及声源方向和声场如何改变。

**亮点：** 显式以动作为条件联合预测视觉与双耳声音，用于视听导航；构建 AVW-4k，提供约 30 小时、76 个室内环境、4,500 条带动作标注的仿真轨迹。其动作条件建模针对导航与声场变化。

**主框架：** 历史图像与双耳声音分别编码 → 输入动作与时间条件 → AV-CDiT 联合预测未来视觉、音频潜在表示 → 解码未来观测 → 辅助连续视听导航。

[论文][avwm]。首次公开于 2025 年，依据 2026 年修订的 v4，重点参考数据、方法与实验部分。

两篇工作的主要区别是：前者侧重历史声音驱动的操作过程预测，后者显式建模动作条件下的视听变化，但验证场景是导航。把后者直接推广为接触操作世界模型，仍需要额外实验支持。

## 三、声音具身数据集与评测

这一类关心数据是否同时包含声音、机器人观测与动作，以及评测能否排除“模型只看图像也能做对”的情况。真实同步录音、后期合成音轨与声场仿真承担不同作用，应分开判断。

### RH20T: A Comprehensive Robotic Dataset for Learning Diverse Skills in One-Shot（2023）

**解决的问题：** 机器人操作学习缺少同时包含真实声音、接触反馈和动作的多模态数据，难以研究声音与动作对齐及复杂接触技能。

**亮点：** 官方报告采集超过 110,000 条真实机器人操作序列，包含视觉、声音、力和运动信息，并提供对应人类示范视频、标定资料与 API，可作为声音参与机器人学习的数据基础。

**主框架：** 多视角相机、麦克风、力传感器与机器人状态同步采集 → 标定并整理为操作序列 → 通过数据加载与处理接口提供多模态示范 → 支持模仿学习和跨模态研究。使用时需逐子集核对音轨、时间戳与许可。

[论文][rh20t] · [项目与数据][rh20t-project] · [API][rh20t-api]。依据 v2 摘要与官方说明，未检查全量数据。

### From Instruction to Event: Sound-Triggered Mobile Manipulation（STMM，2026）

**解决的问题：** 机器人通常接收完整动作指令，缺少从环境声音事件出发，完成导航、操作并消除事件声源的系统性任务与评测。

**亮点：** 提出 STMM 任务、Habitat-Echo 仿真环境和 STMM-12K 数据集，让环境声音触发移动操作，例如先找到声源再完成相应交互。数据包含 18 类声源、453 段真实源声音录音，经声场仿真构成 11,860 个 episode；同时评估规划成功与整条技能链执行成功。

**主框架：** 环境声音与初始 RGB → 高层规划器推断事件并生成技能链 → 导航、抓取等低层技能执行 → 仿真同步更新物体状态与声场，事件解决后相应声音停止。导航技能使用双耳音频与 RGB-D，操作技能主要依靠深度观测。

**适用边界：** 11,860 个 episode 是仿真任务，不能当作真机示范数；系统依赖事件到技能的对应规则、技能库与多事件优先级设置。依据的 v3 仍主要在仿真中验证，并声明代码和数据将在接收后发布，本文不将其标为已开放下载。

[论文][stmm]。依据 v3 的任务、环境、方法、实验及附录；它也属于第一类的声音事件驱动策略。

### SoundSpaces 2.0: A Simulation Platform for Visual-Acoustic Learning（2022，基础平台）

**解决的问题：** 视听导航需要随智能体位置、朝向和环境材质变化的声音，固定位置的预计算声音难以支持连续交互。

**亮点：** 提供实时、空间连续、可配置的声学仿真，支持研究双耳定位、视听导航与声场变化，是构建声音具身任务的基础设施。

**主框架：** 三维室内场景与材质、声源、麦克风配置 → 声学传播与房间脉冲响应渲染 → 与智能体视角同步的音频观测 → 供下游策略训练和评测使用。

**适用边界：** 这是声场渲染平台，不是学习得到的世界模型，也不能替代真实接触操作数据；使用场景资产时还需遵守各自的数据许可。

[论文][soundspaces2] · [项目][soundspaces-project] · [代码][soundspaces-code]。依据原论文与官方平台说明，作为 2023 年之前的必要背景纳入。

### 配套数据与基准一览

下表汇总上述论文配套资源，便于选择研究起点；这些资源不重复计为独立论文。

| 资源与原始来源 | 声音来源 / 任务 | 适合研究什么 | 使用时注意 |
| --- | --- | --- | --- |
| [ManiWAV][maniwav-code] | 人类手持 UMI 采集的真实接触音频、视觉与操作轨迹 | 真实接触反馈、视听策略与跨环境采集 | 是人类手持示范到机器人迁移，区别于真机遥操作数据 |
| [RH20T][rh20t-project] | 真实机器人多模态操作数据 | 视听力融合与动作对齐 | 逐子集核实音轨、时间戳和许可 |
| [OpenX-Sound][openx-sound] / [HEAR-Bench][hear] | 前者为 OXE 视频的合成声音增强；后者用于声音相关操作评测 | 声音预训练、短促事件记忆与响应时机 | 合成音轨不等同于原生物理接触录音 |
| [LIBERO-Audio][listenvla] | 仿真声音操作基准，8 项任务、960 条示范 | 声音条件动作、主动发声感知与音频交换评测 | 数量依据 ListenVLA v1，比较时固定任务与数据版本 |
| [OmniAction][omniaction] | 约 14 万个 episode，包含合成语音、事件声插入与混音 | 上下文意图、主动操作和多模态交互 | 不能把整个语料视为真实同步环境声录制 |
| [AVW-4k][avwm] | 76 个室内环境、4,500 条仿真轨迹，约 30 小时视听数据 | 动作条件视听预测与导航 | 主要描述移动引起的声场变化，非接触操作数据 |
| [STMM-12K / Habitat-Echo][stmm] | 真实源录音经声场渲染的仿真移动操作 episode | 声音事件触发、规划与技能链执行 | v3 声明接收后发布，当前按论文描述使用 |
| [SoundSpaces 2.0][soundspaces-project] | 可配置声场仿真平台 | 连续空间视听导航与数据生成 | 平台、场景资产和下游数据的许可分别核查 |

如果以“声音作为响应信号”为选题，优先比较 **HEAR、ListenVLA、ManiWAV 与 STMM**：分别对应短促事件记忆、声音与动作绑定、接触反馈和事件触发技能链。希望进一步研究“提前响应”，可接着比较第二类中两篇世界模型工作的预测条件与决策接口。这是本文的阅读建议，不代表跨论文统一评测后的性能排名。

[maniwav]: https://arxiv.org/abs/2406.19464v2
[maniwav-project]: https://maniwav.github.io/
[maniwav-code]: https://github.com/real-stanford/maniwav
[hear]: https://arxiv.org/abs/2603.16086v2
[hear-project]: https://hear.irmv.top/
[hear-code]: https://github.com/IRMVLab/HEAR
[openx-sound]: https://huggingface.co/datasets/biubiu2/OpenX-Sound/tree/main
[listenvla]: https://arxiv.org/abs/2610.16313v1
[audio-vla]: https://arxiv.org/abs/2511.09958v1
[roboomni]: https://arxiv.org/abs/2510.23763v3
[roboomni-code]: https://github.com/OpenMOSS/RoboOmni
[omniaction]: https://huggingface.co/datasets/fnlp/OmniAction
[audio-wm]: https://arxiv.org/abs/2512.08405v1
[avwm]: https://arxiv.org/abs/2512.00883v4
[rh20t]: https://arxiv.org/abs/2307.00595v2
[rh20t-project]: https://rh20t.github.io/
[rh20t-api]: https://github.com/rh20t/rh20t_api
[hearing-touch]: https://arxiv.org/abs/2405.08576v1
[hearing-touch-project]: https://sites.google.com/view/hearing-touch
[sonicsense]: https://arxiv.org/abs/2406.17932v2
[sonicsense-project]: https://generalroboticslab.com/SonicSense
[omnivla]: https://arxiv.org/abs/2511.01210v3
[omnivla-code]: https://github.com/GuoHeyu/OmniVLA
[multigen]: https://arxiv.org/abs/2507.02864v2
[multigen-project]: https://multigen-audio.github.io/
[stmm]: https://arxiv.org/abs/2601.21667v3
[soundspaces2]: https://arxiv.org/abs/2206.08312
[soundspaces-project]: https://soundspaces.org/
[soundspaces-code]: https://github.com/facebookresearch/sound-spaces
