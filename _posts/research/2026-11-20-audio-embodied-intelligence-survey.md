---
layout: post
title: "听声而动：声音驱动的机器人策略、VLA、世界模型与数据集调研"
date: 2026-11-20
author: Keith
categories: research
tags: [声音感知, Audio-VLA, VSLA, 世界模型, 多模态数据集, 文献调研]
toc: true
excerpt: "围绕人会根据声音做出响应这一场景，梳理环境事件声、接触声音与语音驱动的机器人策略，重点比较 Audio-VLA、HEAR、ListenVLA、音频世界模型及配套数据。"
---

## 一、先回答问题：有没有类似 VLA、世界模型和数据集的工作？

**有，而且已经出现直接以声音为决策依据的 VLA、音频未来预测模型，以及带声音与动作的数据。** 最贴近“人很多时候会基于声音做出响应”的，不只是语音指令控制，还包括：听到闹钟再去关闭、听倒水声判断何时停止、通过摇晃容器的声音判断里面有什么，以及根据接触声调整操作。

整体链路是：**声音与视觉、本体状态同步观测 → 理解事件或估计隐藏物理状态 → 决定是否行动、何时行动及如何行动 → 执行后继续听取反馈**。世界模型在中间增加“预测未来声音或多模态状态”这一环节。

建议首先阅读六项工作：

| 想回答的问题 | 优先文献 | 核心对应关系 |
| --- | --- | --- |
| 有没有在 VLA 中直接加入接触声音？ | [Audio-VLA][audio-vla] | 视觉、语言、接触音频共同驱动操作 |
| 能不能听到事件后及时响应，而非只听一句指令？ | [HEAR / VSLA][hear] | 流式声音、事件记忆、动作块执行期间的声音留存 |
| 声音能否改变连续动作，还能主动探测？ | [ListenVLA][listenvla] | 声音与动作绑定；听、摇晃、触发后再行动 |
| 有没有“预测未来声音 → 辅助机器人动作”的世界模型？ | [Learning Robot Manipulation from Audio World Models][audio-wm] | 潜空间声音预测，接入机器人策略 |
| 怎样采集真实接触声音和动作示范？ | [ManiWAV][maniwav] | 手持 UMI 加接触麦克风，采集并学习操作 |
| 有没有规模较大、包含真实声音与机器人动作的数据？ | [RH20T][rh20t] | 真实视觉、力、声音与动作序列 |

**调研范围与证据状态：** 整理日期为 **2026-11-20**；重点覆盖 2023 年以来的相关工作，并保留 SoundSpaces 2.0 等必要背景。采用针对性的 arXiv 检索，并沿重点论文的引用查找，不是穷尽式系统综述。重点方法已阅读原文 HTML 的方法、实验和局限部分；RH20T 结合论文摘要、官方项目页与 API 说明核对。文中的实验数值是作者报告，未复现实验；数据规模不等于已下载、完整检查的可训练样本量。官方网页或代码自述的发布状态与已验证可下载状态分开说明。

## 二、先区分声音到底扮演什么角色

### 1. 语音指令：声音承载任务语义

例如“把杯子拿过来”。常见路线是 **语音识别（ASR）→ 文本 → VLA**，也可以把原始语音特征直接送入动作模型。这里主要研究指令理解、口音、多人说话、语调、打断和响应延迟。

**它不自动证明机器人会听接触声或感知物理过程。** 只把语音转成文字，可能丢掉敲击、摩擦、报警、液体流动等非语言信息。Speech-π₀.₅ 和 VoiceGuard 属于这一侧，见后文补充阅读。[S1][speech-action] [S2][voiceguard]

### 2. 环境事件声：声音决定目标和行动时机

例如“闹钟响了再关掉”“找到正在发声的设备”。声音可提供事件类别、目标位置和触发时刻，适合 HEAR、ListenVLA 和 Sound-Triggered Mobile Manipulation（STMM）这类研究。[3][hear] [4][listenvla] [10][stmm]

### 3. 接触声与结构振动：声音提供物理状态反馈

例如擦拭、翻动物体、卡扣闭合、物体滑移，以及摇晃容器。麦克风可以接收空气传播声，也可以贴在夹爪或手指上记录结构传导振动。后者与触觉接近，但不能把普通环境录音、接触麦克风和力传感器当成可直接互换的输入。

ManiWAV、Audio-VLA、FuSe 和 SonicSense 分别对应数据采集、动作学习、异构传感器适配及主动物体感知。[1][maniwav] [2][fuse] [5][audio-vla] [9][sonicsense]

### 4. 未来声音：声音是要预测的状态

“现在听到什么”与“接下来会听到什么”是不同问题。预测倒水声的演化，可以帮助策略提前判断停止时机；预测机器人移动后的双耳声音，可以用于空间推理和导航。[7][audio-wm] [8][avwm]

为避免混淆，以下用 \(s_t\) 表示声音、\(v_t\) 表示视觉、\(q_t\) 表示机器人状态、\(l\) 表示语言、\(u_t\) 表示控制动作：

- **声音条件策略：** \(u_{t:t+H} \sim \pi(v_{\leq t},s_{\leq t},q_t,l)\)。回答下一步怎么做。
- **声音未来预测：** \(\hat{s}_{t+1:t+H}\sim p_\theta(s_{t+1:t+H}\mid s_{\leq t},\ldots)\)。回答声音将如何发展，具体条件由论文决定。
- **动作条件多模态世界模型：** \((\hat v,\hat s)_{t+1:t+H}\sim p_\theta(\cdot\mid v_{\leq t},s_{\leq t},u_{t:t+H-1})\)。可以比较不同动作的预测后果。

**判断边界：** 声音重建器、声音分类器和视频配音模型本身不等于可用于控制的世界模型；预测未来声音也不必然支持“换一个动作会怎样”的反事实推演。后文会明确区分。

## 三、重点策略文献：从听到声音到生成动作

### 1. ManiWAV：真实接触声音与动作学习的直接起点

**ManiWAV: Learning Robot Manipulation from In-the-Wild Audio-Visual Data**，首次公开 2024-06-27；本文依据 arXiv v2。[论文][maniwav] · [项目][maniwav-project] · [代码][maniwav-code]

**问题与方法：** 传统视动策略在接触过程被遮挡、视觉变化不明显时，很难判断接触状态。ManiWAV 在 UMI 手持采集设备上加入接触麦克风，形成“ear-in-hand”，同步采集图像、声音和手持操作轨迹；视觉与声音特征融合后，通过扩散策略输出动作。

**原文证据：** 方法部分介绍硬件、音频表示与融合；实验覆盖白板擦拭、锅铲翻贝果、从杯中倒出物体、魔术贴捆线四类任务。其中倒出物体不是液体倒水。作者还测试了噪声、配置变化和未见采集环境。

**为什么相关：** 它验证了声音可以直接参与闭环操作，也提供了采集路径。**边界：** 它是任务驱动的音视模仿学习系统，不是通用语言条件 VLA，也没有显式未来世界模型；不同传感器安装位置和人手到机器人的振动差异仍需处理。

### 2. FuSe：让已有通用策略适配声音等异构传感器

**Beyond Sight: Finetuning Generalist Robot Policies with Heterogeneous Sensors via Language Grounding**，首次公开 2025-01-08；依据 v3。[论文][fuse] · [项目][fuse-project] · [代码][fuse-code] · [数据入口][fuse-data]

**问题与方法：** 大量预训练策略主要见过视觉与机器人状态，而带触觉、音频的数据较少。FuSe 以自然语言作为跨模态语义接口，结合多模态对比学习和感知条件语言生成，微调已有通用策略，使其使用新增传感器。

**原文证据：** §III 给出适配目标，§IV 包含真实机器人、多模态提示、跨模态组合与 VLA 实验。官方代码说明发布了 **26,866 条机器人轨迹**；这是异构传感器数据总量，不能解释成每条都包含所有模态的等量音频样本。

**为什么相关：** 如果目标是给已有 VLA 增加“听觉”，它比从零预训练多模态大模型更适合作为方法参考。**边界：** 高层语言对齐是否保留毫秒级接触时序，要另行验证；不是声音未来预测模型。

### 3. HEAR / VSLA：专门处理“声音短促，但机器人来不及听”的问题

**Towards the Vision-Sound-Language-Action Paradigm: The HEAR Framework for Sound-Centric Manipulation**，首次公开 2026-03-17；依据 2026-09-18 的 v2。[论文][hear] · [项目][hear-project] · [代码][hear-code]

**问题与方法：** 相机里的物体往往持续存在，而“滴”“咔哒”等声音可能在动作块执行期间出现又消失。论文将这种错过声音的执行间隔形式化为 **Blind Execution Interval（BEI）**，提出视觉—声音—语言—动作（VSLA）框架：

- **Historizer：** 在执行间隙持续汇总声音，保留事件证据。
- **Envisioner：** 联合视觉、声音与语言推理任务阶段。
- **Advancer：** 训练时预测近未来声音 token，提供时间对齐监督；部署时移除。
- **Realizer：** 通过流匹配生成连续动作块。

**原文证据：** §3 分析时序与因果评估；§4 介绍架构；§5 给出 OpenX-Sound 和 HEAR-Bench；§6 在七个仿真任务及四个真实 Franka 任务上评估。作者报告 HEAR-Bench 成功率 **81%**，真实任务的声音因果成功率 **70%**。评测要求动作发生在相关声音之后，不能提前完成几何目标就算成功。

**为什么相关：** 对“听声响应”的研究问题非常直接，尤其适合关注声音触发、过程监控与时序。**边界：** 未来声音模块是训练辅助目标，不能把它写成部署时进行候选动作搜索的完整世界模型。其 OpenX-Sound 音轨是合成增强，不能等同实录接触物理。

### 4. ListenVLA：声音与动作绑定，以及主动获取声音证据

**Listen Before Act: Audio-Conditioned Robot Manipulation with ListenVLA**，首次公开 2026-10-12；依据 v1。[论文][listenvla] · [作者提供的匿名代码入口][listenvla-code]

**问题与方法：** 在模型里加入音频特征，不代表它真的依据声音做动作。ListenVLA 基于 GR00T N1.7，将语义声音嵌入与波形导出的声学线索组成因果历史，通过音频 token 和特征调制影响连续动作生成；额外加入 **audio–action binding** 目标，在匹配的非音频上下文中约束声音差异与动作差异的关系。

**原文证据：** §III-D 定义 **LIBERO-Audio 八项任务**，包括发声目标选择、延迟闹钟、摇晃盒子以及先触发再关闭蜂鸣器；§IV-A 给出 **960 条示范**，§IV-C 和 §IV-D 分别做消融与音频交换测试。表 II 报告八任务平均成功率 **66.25%**；表 III 中去掉绑定目标后为 **38.25%**。不过主动探测的 T5、T8 分别只有 **32%**、**20%**，不能把平均结果理解成主动听觉已经解决。另有三项真实机器人任务。

**为什么相关：** “先动一下获得声音，再依据声音行动”是很有价值的主动感知范式。**边界：** 音频交换引起动作变化，只证明音频影响预测，仍需结合任务成功与时序测试判断影响是否正确。本文访问匿名代码入口返回 401，**未确认代码、权重和数据是否可实际取得**。

### 5. Audio-VLA：把接触声音直接加进 VLA

**Audio-VLA: Adding Contact Audio Perception to Vision-Language-Action Model for Robotic Manipulation**，首次公开 2025-11-13；依据 v1。[论文][audio-vla]

**问题与方法：** 用接触音频补足视觉对交互过程的感知。论文采用 DINOv2、SigLIP 视觉编码器，AudioCLIP 音频编码器和 Llama2 主干，通过投影对齐与 LoRA 微调形成多模态动作策略；在 LIBERO、RLBench 中增加碰撞相关音频反馈。

**原文证据：** §III 介绍架构及 Task Completion Rate（TCR）过程指标；§IV 包括 LIBERO、五项 RLBench 任务和两项真实任务。表 I 的标准环境均值分别为 **97.6%（LIBERO）**、**55.1%（五项 RLBench）**；表 IV 的视觉单模态消融与完整模型也有差异。

**为什么相关：** 这是“有没有声音版 VLA”的直接肯定证据。**边界：** 它是声音条件策略，不是世界模型；仿真碰撞音不能自动代表真实摩擦、滑移或液体声。本次原文中未定位到可核实的官方代码、权重和数据发布入口，复现可得性待核实。

### 6. RoboOmni：从对话、环境声和视觉上下文推断该做什么

**RoboOmni: Proactive Robot Manipulation in Omni-modal Context**，首次公开 2025-10-27；依据 v3。[论文][roboomni] · [代码与模型说明][roboomni-code] · [OmniAction 数据入口][omniaction]

**问题与方法：** 用户未必直接发出命令，机器人需要结合多人对话、非语言声音及视觉推断意图。RoboOmni 使用 Perceiver–Thinker–Talker–Executor 架构，将意图识别、交互确认、语音与动作输出放入统一框架。

**原文证据：** §3 介绍 OmniAction，§4 介绍模型；官方 README 列出约 **14 万条 episode**、六类上下文指令，以及模型、数据和 LIBERO 评测入口。其数据构建会改写已有轨迹指令，并用语音合成、多说话人混音、事件声音插入与背景混音生成声音上下文。

**为什么相关：** 适合“听到一个情境后主动帮忙”，而不限于逐字执行命令。**边界：** OmniAction 的事件声和对话主要是合成增强，不能解释成 14 万条真实接触音频示范。自主推断用户意图与接触力学感知也应分开评估。

### 7. 其他值得纳入视野的策略与感知工作

| 工作 | 原文验证的能力或机制 | 对本问题的用途与边界 |
| --- | --- | --- |
| [SonicSense（2024）][sonicsense] | 在手声振动感知；83 个真实物体上的材料、形状、容器内容状态等推断 | 主动敲击、探索以获得隐藏属性；主要是物体感知，不是通用 VLA |
| [STMM（2026）][stmm] | Habitat-Echo 中根据声音事件规划技能链，再导航并操作；提出 STMM-12K | 很贴近“听到事情发生再响应”；仿真分层任务，非机械臂端到端通用策略 |
| [MuSTMM（2026）][mustmm] | 将声音触发移动操作扩展到 31 个场景，做场景隔离评测 | 可研究未见建筑结构的泛化；论文仍写接收后发布，未核实可下载 |
| [MuseVLA（2026）][musevla] | 按需调用传感器，将声源定位等测量转为与 RGB 对齐的 grounded sensor image | 提供“声学热图 → VLA”的接口；不等于直接用原始波形学习接触动力学 |
| [PolyUMI（2026）][polyumi] | 手持采集视觉、触觉、接触声音，并评估隐藏物体推断和闭环滑移控制 | 适合作为采集平台参考；传感器组合收益不能全部归功于音频 |
| [S2A2（2026）][s2a2] | 将声学空间信息与频谱信息结合，用于声源定位、识别和音视模仿操作 | 适合多声源目标选择；是音视动作学习，不应直接归为语言条件 VLA |

补充工作均以链接中的论文或项目为依据；不据此推断它们已经适配当前仓库讨论过的 Cruzr S2。

## 四、声音世界模型：已有直接工作，但能力层级不同

### 1. Learning Robot Manipulation from Audio World Models：最直接的音频预测到操作

**Learning Robot Manipulation from Audio World Models**，Fan Zhang、Michael Gienger，首次公开 2025-12-09；依据 v1。[论文][audio-wm]

**方法链路：** 将历史音频转成频谱表示 → 用编码器学习声音潜空间 → 通过潜空间流匹配生成未来声音 → 将当前图像、当前声音与预测声音交给动作策略。声音模型与动作策略分阶段训练。

**原文证据：** §2 给出预测和策略结构；§3.1 用 Kinova Gen3 按压、松开饮水机按钮控制注水，作者报告 **30 次测试全部成功**；§3.2 是仿真钢琴场景，以未来音乐信息辅助 SAC 策略。注水场景的约 50 ms 模型预测耗时是作者特定设置结果，不能当成任意平台的控制性能保证。

**为什么重要：** 它直接回答“有没有声音的世界模型用于机器人”，而不只是音频分类或配音。

**必须保留的边界：** 按其方法定义，声音预测主要由历史音频条件驱动，并未展示通用的候选控制动作条件反事实推演。因而更准确地称为**面向特定过程的声音未来预测器，辅助策略前瞻**；30 次同类任务成功也不能外推为跨容器、跨流速或跨机器人泛化。本次未定位到已核实的官方训练代码、权重和数据入口。

### 2. Audio-Visual World Models / AV-CDiT：动作条件的视听未来预测

**Audio-Visual World Models: Learning Physically Grounded Multisensory Dynamics**，首次公开 2025-11-30；依据 2026-08-04 的 v4。[论文][avwm]

**方法链路：** 历史视觉与双耳声音 + 动作/时间条件 → AV-CDiT 联合预测未来视觉、声音 → 辅助连续视听导航。其 formulation 显式包含动作条件，比仅做历史声音续写更接近可用于规划的世界模型。

**原文证据：** “Formulation and Dataset”给出定义和 **AVW-4k**；数据来自 Matterport3D 与 SoundSpaces 2.0 仿真，约 **30 小时、76 个室内环境、4,500 条轨迹**。“Methodology”和实验部分介绍模型、预测指标与导航应用。数据名称中的“4k”不应当作精确轨迹数。

**边界：** 这里的动作与物理变化主要是移动、视点和声场变化，不是机械臂接触操作。它能启发“移动后听到什么”的研究，但不能直接证明会预测插接、滑移或接触力。本次原文中未定位到可核实的官方代码与数据下载入口。

### 3. Dreaming the Sound of Contact：生成声音作为接触控制先验

**Dreaming the Sound of Contact: Leveraging Video and Audio Generation for Zero-Shot Force-Aware Manipulation and Data Generation**，首次公开 2026-09-16；依据 v2。[论文][dream-contact] · [项目与数据入口][dream-contact-project]

**方法与证据：** 联合利用生成的视频和接触音频：由视频导出运动轨迹，由生成声音的响度塑造目标力曲线，再用真实 Franka 的闭环力调节器执行。论文还展示由该流程生成数据以训练闭环策略。

**定位：** 与多模态世界生成和机器人数据生成相关，但不是“当前麦克风声音直接到动作”的同一种设置。其闭环接触力依赖力反馈，**声音响度与接触力的任务相关映射不能当成通用力学定律**，更不能直接移植到未标定的材料和麦克风。

### 4. AudioWorldSim 与 BinauralVAE：基础设施，不是已完成的控制世界模型

- [AudioWorldSim（2026）][audio-world-sim] 基于 SoundSpaces 2.0 自动采集导航轨迹下的双耳音频，提供生成世界模型训练数据的工具。[官方代码][audio-world-sim-code]
- [BinauralVAE（2026）][binaural-vae] 研究双耳音频压缩与重建，为潜空间表示提供基础。[官方代码入口][binaural-vae-code]

两者可帮助搭建声音世界模型，但 **VAE 能重建声音，不等于已经学会动作导致的未来状态，也不等于已有闭环控制收益**。后者原文也将完整音频世界模型作为后续目标。

## 五、数据集怎么选：先看有没有同步动作，再看声音从哪里来

### 1. 可用于策略或世界模型研究的资源

| 数据 / 基准 | 声音与其他输入 | 动作或监督 | 更适合做什么 | 发布与使用边界 |
| --- | --- | --- | --- | --- |
| [RH20T][rh20t-project]（2023） | 真实多视角视觉、声音、力与机器人状态 | 真实机器人动作、对应人类示范视频 | 真实接触操作、多模态状态估计、音频动作对齐 | 官方提供数据下载与 API；需核对各子集实际音轨。许可分 RH20T-C / NC，不能把整套都视作可商用 |
| [ManiWAV][maniwav-code]（2024） | 真实接触音频与视觉 | UMI 操作轨迹，可用于机器人模仿学习 | 擦拭、翻动、倒物体、捆扎等接触反馈 | 官方代码 README 有数据入口；需处理手持到机器人与传感器安装差异 |
| [FuSe][fuse-data]（2025） | 真实异构传感器，包含视觉、触觉或音频 | 机器人动作与语言相关监督 | 给预训练策略接入新传感器 | 官方项目、代码列有数据与模型；总 26,866 条轨迹不等于全部都有音频，按子集选用 |
| [OmniAction / OmniAction-LIBERO][omniaction]（2025） | 轨迹视觉配合合成对话、事件声与背景声 | 机器人动作和上下文指令 | 意图理解、多说话人、环境事件语义到动作 | 官方代码列有 Hugging Face 发布入口；本次未完整下载检查。不是实录接触声库 |
| [OpenX-Sound][openx-sound]（2026） | 保留所选 OpenX 轨迹，为视频合成时间对齐声音 | 原有动作、语言、本体状态 | 声音与机器人时序对齐预训练 | 官方项目与代码列有发布入口；本文未直接访问完整 HF 数据。不是把原始 OXE 缺失的录音找回来了 |
| HEAR-Bench（2026） | 基于 RoboTwin2，事件条件声音流 | 七项声音因果任务与时序成功条件 | 瞬态声音响应、等待与过程监控 | 见 [HEAR 原文 §5.2][hear] 和 [代码入口][hear-code]；具体资源完整性需按发布版本检查 |
| LIBERO-Audio（2026） | 音频渲染、视觉、指令、本体状态 | 八任务、960 条示范 | 声音选目标、延迟响应、主动探测 | [ListenVLA 原文][listenvla] 已描述；匿名代码入口本次返回 401，下载待核实 |
| STMM-12K / MuSTMM（2026） | 仿真双耳声音、场景观测 | 移动、交互技能链和任务评估 | 声音触发的导航加操作 | 原文分别报告约 11.86k episode、31 场景扩展；都写接收后发布，本次未核实下载 |
| AVW-4k（2025/2026） | 仿真同步双耳音频与视觉 | 导航动作与未来观测 | 动作条件视听预测、导航规划 | [原文][avwm] 报告约 30 小时、4,500 条轨迹；本次未定位官方数据下载入口 |
| [AudioWorldSim][audio-world-sim-code]（2026） | 仿真连续双耳声音与环境观测 | 导航轨迹、动作及相关元数据，依具体配置 | 自建音频动力学与空间听觉数据 | 官方代码可访问；属于数据生成平台，不等于现成通用 VLA 数据集 |

**选型结论：** 做真实接触反馈先看 **ManiWAV、FuSe、RH20T**；做声音触发动作先看 **HEAR-Bench、LIBERO-Audio**；做语音与情境语义先看 **OmniAction**；做动作条件视听世界模型先看 **AVW-4k、AudioWorldSim**。它们不应混成一个统一排行榜。

### 2. 哪些相关数据不能直接叫作 VLA 数据？

- **AudioSet、VGGSound 等声音事件/音视频数据：** 可用于声音编码器预训练，但通常不提供与录音同步的机器人控制动作，不能单独完成 VLA 行为克隆。
- **SoundSpaces 2.0：** 是声学渲染与视听学习平台，可生成带导航交互的数据；不天然提供机械臂接触动作。[11][soundspaces]
- **物体声音或材料识别数据：** 可以学习隐藏属性，但属性标签与连续控制轨迹是不同监督。
- **原版 Open X-Embodiment、LIBERO 或 RLBench：** 不能仅凭名字断言包含可用的真实麦克风音轨；OpenX-Sound、LIBERO-Audio 和 Audio-VLA 的音频增强都是额外工作。

对于任何“带声音”的候选数据，应先抽查：**原始波形是否存在、采样与时间戳是否可靠、音频和动作如何对齐、动作是人手位姿还是机器人控制量、是否有语言指令、成功/失败是否标注、训练测试是否共享物体或录音、许可是否适用。** 本文没有把未下载的子集计为已验证可训练数据。

## 六、横向判断：已经有先例，真正值得研究的是什么？

以下是依据文献归纳的研究判断，**不是任何单篇论文已经证明的结论**。

### 1. “VLA 加音频编码器”本身已不足以构成明显新问题

Audio-VLA、FuSe、HEAR、ListenVLA 都已有相关设计。更有区分度的问题包括：

- **时间响应：** 声音发生在动作块执行期间，怎样保存并及时使用？比较 HEAR 的事件留存与普通滑动窗口。
- **主动听觉：** 面对外观相同的容器，如何决定先摇晃、敲击还是直接操作？结合 ListenVLA、SonicSense 和 UMI 采集路线。
- **声音确实参与决策：** 固定视觉、语言、状态和采样随机性，只交换或延迟声音，动作与完成时机是否按预期变化？
- **真实泛化：** 换材料、房间、麦克风位置、背景噪声和机器人后，是否仍可用？不能只在同一组音频片段上随机切分。
- **音频预测是否值得：** 在相同数据、模型容量与推理预算下，显式未来预测是否胜过只加长声音历史？

### 2. 世界模型要先说明预测什么、条件是什么、如何帮助动作

可以区分三个研究层级：

1. **状态估计：** 从声音判断空满、接触、滑移或异常；输出属性/事件，不预测未来。
2. **未来辅助策略：** 预测后续声音或事件表示，输入策略，或作为训练辅助损失；音频世界模型论文和 HEAR 分别提供不同实现。
3. **动作条件规划：** 输入不同候选动作，预测不同视听后果，再选择动作；AVWM 在导航中提供参考，接触丰富的真实操作仍需新的验证。

对早期课题，先比较第一、第二层通常更易建立清晰证据。若要声称第三层，必须展示动作干预有效、预测跨动作可靠，以及闭环执行确实受益。

### 3. 与现有 Cruzr S2 场景的联系

仓库此前讨论的是“流水线抓取 → 移到扫码位 → 根据编码放置”。**本文建议**先把声音用于可解释的状态反馈，例如抓取/放置碰撞、疑似掉落、设备提示音与异常事件；前提是这些声音对任务有稳定信息。

若扫码器存在可配置的提示音，可以研究完成事件响应，但不能假设当前设备一定有此接口。声音也不能替代读取二维码内容：**编码到放置位置的映射仍需扫码结果**。已有论文未证明其模型能直接部署到 Cruzr S2。

## 七、建议的阅读与最小验证路线

**阅读顺序：** ManiWAV → FuSe → Audio-VLA → HEAR → ListenVLA → Learning Robot Manipulation from Audio World Models → AVWM；若更偏服务机器人“听到事情再去处理”，提前阅读 STMM 和 RoboOmni。

最小验证可选“外观相同容器的声音辨别”“听到延迟提示音后再操作”或“根据过程声停止”之一，先避免把导航、对话、主动探索和精细操作全部揉在一起。下面是待实施的实验建议：

| 对照组 | 回答的问题 |
| --- | --- |
| 视觉 + 本体状态；需要时加相同语言指令 | 不听声音时能做到什么程度？ |
| 上述输入 + 声音历史 | 声音本身是否提供额外信息？ |
| 上述输入 + 更长历史或事件记忆 | 收益是不是仅来自记住过去？ |
| 上述输入 + 未来声音/事件预测 | 在相同预算下，前瞻是否还有增益？ |
| 静音、错配、延迟音频；随机化声音触发时刻 | 模型是否靠声音作出正确且及时的响应？ |

除整任务成功率，还应记录事件发生到动作响应的延迟、提前动作率、漏响应率、过程停止误差、噪声与传感器变化下的性能，以及额外推理耗时。所有输入必须只使用决策时刻已经收到的声音，不能把未来实录音频误当成在线观测。

这条路线可以形成清楚的问题：**在视觉无法充分判断状态时，声音历史、事件记忆和未来预测，分别为机器人闭环决策提供了多少可验证增益？**

## 八、原始来源与核实说明

下列日期为首次公开时间；正文已注明所读修订版本，不能把不同版本的方法或数值混用。未核实会议或期刊元数据的条目按 arXiv 论文引用；HEAR 项目页自述已被 IJRR 接收，本文仍以所读预印本为方法与数值依据。

1. **ManiWAV**，2024-06-27。[论文][maniwav]；重点：方法、四项操作实验与附录。[项目][maniwav-project]、[代码及数据说明][maniwav-code]已访问。
2. **Beyond Sight / FuSe**，2025-01-08。[论文][fuse]，§III–IV；[项目][fuse-project]、[代码][fuse-code]已访问，数据入口依据官方链接，未完整下载。
3. **HEAR / VSLA**，2026-03-17。[论文][hear]，v2 §3–6；[项目][hear-project]、[代码 README][hear-code]与 OpenX-Sound 发布链接已核对，未完整下载数据。
4. **ListenVLA**，2026-10-12。[论文][listenvla]，§III-D、§IV、表 II–III；[匿名代码入口][listenvla-code]返回 401，资源可得性待核实。
5. **Audio-VLA**，2025-11-13。[论文][audio-vla]，§III–IV、表 I 与 IV；未定位到已核实的官方代码/数据入口。
6. **RoboOmni**，2025-10-27。[论文][roboomni]，§3–4 与实验；[官方代码 README][roboomni-code]已访问，模型和数据入口依该说明，未完整下载。
7. **Learning Robot Manipulation from Audio World Models**，2025-12-09。[论文][audio-wm]，§2–3；未定位到已核实的官方代码/数据入口。
8. **Audio-Visual World Models**，2025-11-30。[论文][avwm]，v4 的 Formulation and Dataset、Methodology 与实验；未定位到已核实的官方代码/数据入口。
9. **SonicSense**，2024-06-25。[论文][sonicsense]，方法与物体感知实验；是感知系统，非通用 VLA。
10. **From Instruction to Event / STMM**，2026-01-29。[论文][stmm]，v3 §3–6；[MuSTMM][mustmm] 首次公开 2026-10-15。二者原文仍写接收后发布。
11. **SoundSpaces 2.0**，2022-06-16。[论文][soundspaces]。作为声学模拟基础背景引用。
12. **RH20T**，2023-07-02。[论文][rh20t]摘要、[官方项目][rh20t-project]与 [API][rh20t-api]；规模、模态与许可依据官方说明，未检查全量音轨。
13. **MuseVLA**，2026-06-16。[论文][musevla]与[官方代码][musevla-code]；注意其声学热图接口与原始波形输入的区别。
14. **Dreaming the Sound of Contact**，2026-09-16。[论文][dream-contact]与[项目][dream-contact-project]；项目提供数据链接，未完整下载。
15. **AudioWorldSim**，2026-08-21。[论文][audio-world-sim]、[代码][audio-world-sim-code]；**BinauralVAE**，2026-09-06。[论文][binaural-vae]、[代码入口][binaural-vae-code]，属于音频表示与仿真基础。
16. **PolyUMI**，2026-09-24。[论文][polyumi]与[项目][polyumi-project]；**S2A2**，2026-07-28。[论文][s2a2]。作为声音采集、触觉融合及声源空间信息的补充阅读。

语音驱动补充：

- **S1. Audio-Language-Action Models with Direct Speech Conditioning / Speech-π₀.₅**，2026-10-24。[原文][speech-action]为 Late Breaking Results 短文，介绍在 π₀.₅ 上直接处理语音；不据此推断接触声感知能力。
- **S2. VoiceGuard**，2026-11-15。[原文][voiceguard]，音频原生 LLM、结构化请求校验与 SmolVLA 执行的辅助机械臂流水线；属于语音接口与执行编排，非接触音频世界模型。

**检索词：** audio-conditioned robotic manipulation、contact audio policy、vision-sound-language-action、audio-action binding、sound-triggered mobile manipulation、audio world models、action-conditioned audio-visual dynamics、multisensory robot dataset。资源状态随作者发布更新；未验证条目保留为后续核查项。

[maniwav]: https://arxiv.org/abs/2406.19464v2
[maniwav-project]: https://maniwav.github.io/
[maniwav-code]: https://github.com/real-stanford/maniwav
[fuse]: https://arxiv.org/abs/2501.04693v3
[fuse-project]: https://fuse-model.github.io/
[fuse-code]: https://github.com/fuse-model/FuSe
[fuse-data]: https://huggingface.co/datasets/oier-mees/FuSe
[hear]: https://arxiv.org/abs/2603.16086v2
[hear-project]: https://hear.irmv.top/
[hear-code]: https://github.com/IRMVLab/HEAR
[openx-sound]: https://huggingface.co/datasets/biubiu2/OpenX-Sound/tree/main
[listenvla]: https://arxiv.org/abs/2610.16313v1
[listenvla-code]: https://anonymous.4open.science/r/listenvla-F18D/
[audio-vla]: https://arxiv.org/abs/2511.09958v1
[roboomni]: https://arxiv.org/abs/2510.23763v3
[roboomni-code]: https://github.com/OpenMOSS/RoboOmni
[omniaction]: https://huggingface.co/datasets/fnlp/OmniAction
[audio-wm]: https://arxiv.org/abs/2512.08405v1
[avwm]: https://arxiv.org/abs/2512.00883v4
[sonicsense]: https://arxiv.org/abs/2406.17932v2
[stmm]: https://arxiv.org/abs/2601.21667v3
[mustmm]: https://arxiv.org/abs/2610.21429v1
[soundspaces]: https://arxiv.org/abs/2206.08312
[rh20t]: https://arxiv.org/abs/2307.00595v2
[rh20t-project]: https://rh20t.github.io/
[rh20t-api]: https://github.com/rh20t/rh20t_api
[musevla]: https://arxiv.org/abs/2606.17598v2
[musevla-code]: https://github.com/microsoft/MuseVLA
[dream-contact]: https://arxiv.org/abs/2609.19137v2
[dream-contact-project]: https://dreamingcontactsound.github.io/
[audio-world-sim]: https://arxiv.org/abs/2608.21075v1
[audio-world-sim-code]: https://github.com/Luizerko/AudioWorldSim
[binaural-vae]: https://arxiv.org/abs/2609.06837v1
[binaural-vae-code]: https://github.com/Luizerko/BinauralVAE
[polyumi]: https://arxiv.org/abs/2609.29760v2
[polyumi-project]: https://polyumi-vista.github.io/
[s2a2]: https://arxiv.org/abs/2607.26047v2
[speech-action]: https://arxiv.org/abs/2610.33866v1
[voiceguard]: https://arxiv.org/abs/2611.19984v1
