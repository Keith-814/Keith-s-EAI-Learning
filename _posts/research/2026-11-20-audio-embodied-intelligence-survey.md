---
layout: post
title: "声音驱动机器人文献调研"
date: 2026-11-20
author: Keith
categories: research
tags: [声音感知, Audio-VLA, VSLA, 世界模型, 多模态数据集, 文献调研]
toc: true
excerpt: "整理声音驱动机器人操作、视觉声音语言动作模型、音频世界模型及相关数据集，介绍各项工作的研究问题、系统框架、主要创新与局限。"
---

这组文献的主线可以概括为：先利用声音补充视觉难以观测的接触状态和物体属性；再将声音、视觉、语言与机器人状态结合，生成连续动作或响应环境事件；最后通过预测未来声音与视听状态，支持过程监控、动作前瞻和规划。相关数据既包括真实机器人录音，也包括合成音频增强和声学仿真，三者的用途与验证范围不同。

语音指令、环境事件声和接触声音承担不同作用。语音主要表达任务意图；报警、提示音等事件声决定目标与行动时机；碰撞、摩擦和结构振动则提供物理交互反馈。下文先介绍声音感知与动作策略，再介绍世界模型、数据资源和语音接口。

调研日期为 2026-11-20，重点覆盖 2023 年以来的相关工作。论文链接固定到本次阅读的版本；未核实正式发表信息的工作按 arXiv preprint 标注。实验结果均为作者报告，未复现实验，数据和代码的可得性按本次核查状态说明。

## 1. ManiWAV: Learning Robot Manipulation from In-the-Wild Audio-Visual Data（2024，arXiv preprint）

该工作解决了视觉策略难以判断接触状态，以及带声音的操作示范难以在真实环境中采集的问题。擦拭、翻动物体和倾倒等任务的视觉变化可能不明显，接触声音能够补充接触发生、运动方式和物体状态的信息。

系统在 UMI 手持采集设备上加入接触麦克风，同步记录图像、声音和操作轨迹。模型分别提取视觉与音频特征，融合后通过扩散策略生成动作，并在执行过程中持续利用新观测修正。论文评估了白板擦拭、锅铲翻贝果、从杯中倒出物体和魔术贴捆线四类任务，以及噪声和环境变化下的表现。

它的主要创新是将接触声音采集与手持操作示范结合，使声音能够直接参与机器人模仿学习。局限是人手采集与机器人执行之间仍存在振动和传感器安装差异，策略也依赖任务示范；它不是通用语言条件 VLA，未显式建模未来状态。

[论文][maniwav] · [项目][maniwav-project] · [代码与数据说明][maniwav-code]。依据 v2 的方法、实验与附录。

## 2. SonicSense: Object Perception from In-Hand Acoustic Vibration（2024，arXiv preprint）

该工作解决了仅凭外观难以判断物体材料、容器内容状态和内部属性的问题。对于不透明容器或外观相似的物体，机器人需要通过交互获得额外的物理信息。

系统利用在手声振动传感器记录与物体交互时产生的信号，通过探索动作采集声音，再由学习模型融合信号并推断物体属性。论文在 83 个真实物体上评估了容器内容状态区分、异质材料预测、三维形状重建和物体重识别。

它的主要创新是把主动交互与在手声振动感知结合，扩展了机器人获取隐藏物理属性的方式。局限是探索策略主要采用启发式设计，方法重点是物体感知，不能直接视为语言条件动作模型或世界模型。

[论文][sonicsense]。依据 v2 的方法与物体感知实验。

## 3. Beyond Sight: Finetuning Generalist Robot Policies with Heterogeneous Sensors via Language Grounding（2025，arXiv preprint）

该工作解决了预训练机器人策略难以接入音频、触觉等新传感器的问题。现有大规模数据主要包含视觉和本体状态，而多传感器示范数量较少，难以直接重新训练通用策略。

系统提出 FuSe，以自然语言作为不同传感器之间的语义接口，通过多模态对比学习和感知条件语言生成，将新增传感器与已有策略对齐。该训练方法能够适配扩散式通用策略和 VLA，论文在真实机器人上评估了多模态提示、跨模态组合和操作任务。

它的主要创新是利用语言对齐降低异构传感器适配的难度，提供了给已有通用策略增加听觉的训练路线。局限是高层语义对齐能否保留精细接触时序仍需验证；官方发布的 26,866 条轨迹属于异构传感器数据总量，不能理解成每条都包含音频和所有传感器。

[论文][fuse] · [项目][fuse-project] · [代码][fuse-code] · [数据][fuse-data]。依据 v3 §III–IV 与官方发布说明。

## 4. Audio-VLA: Adding Contact Audio Perception to Vision-Language-Action Model for Robotic Manipulation（2025，arXiv preprint）

该工作解决了视觉语言动作模型对接触事件和操作过程感知不足的问题。仅依赖图像时，机器人可能难以判断物体是否接触、交互是否完成，以及动态过程是否发生变化。

系统采用 DINOv2、SigLIP 视觉编码器、AudioCLIP 音频编码器和 Llama2 主干，通过多模态投影与 LoRA 微调，将视觉、语言和接触声音共同用于动作预测。论文在 LIBERO 和 RLBench 中增加碰撞相关音频反馈，并在两项真实任务中进行验证，同时提出 Task Completion Rate（TCR）评价操作过程。

它的主要创新是将接触声音直接引入 VLA 的感知与控制链路。原文表 I 报告标准环境下 LIBERO 平均成功率为 97.6%，五项 RLBench 任务平均为 55.1%。局限是仿真碰撞音不能完整代表真实摩擦、滑移和液体声；该方法仍是声音条件策略，本次未定位到已核实的官方代码和数据入口。

[论文][audio-vla]。依据 v1 §III–IV、表 I 与表 IV。

## 5. Towards the Vision-Sound-Language-Action Paradigm: The HEAR Framework for Sound-Centric Manipulation（2026，arXiv preprint）

该工作解决了机器人在动作块执行期间容易遗漏短促声音的问题。图像中的物体通常持续可见，而提示音、碰撞声等信号可能在两次策略更新之间出现并消失，使模型无法确定动作触发时机。

系统提出视觉—声音—语言—动作（VSLA）框架 HEAR。Historizer 持续汇总声音并保留事件证据，Envisioner 进行多模态任务推理，Advancer 在训练时预测近未来声音 token，Realizer 通过流匹配生成连续动作块。论文同时构建 OpenX-Sound 和 HEAR-Bench，并在七项仿真任务和四项真实 Franka 任务中评估。

它的主要创新是将声音留存、时间对齐和连续动作生成结合，显式处理动作执行间隔中的感知缺口。原文 §6 报告 HEAR-Bench 成功率为 81%，真实任务的声音因果成功率为 70%。局限是 OpenX-Sound 使用合成音轨，真实声学泛化仍需验证；Advancer 在部署时移除，不能将其视为在线搜索候选动作的完整世界模型。

[论文][hear] · [项目][hear-project] · [代码][hear-code] · [OpenX-Sound][openx-sound]。依据 v2 §3–6；项目页自述已被 IJRR 接收，本文方法与数值仍以该预印本为依据。

## 6. Listen Before Act: Audio-Conditioned Robot Manipulation with ListenVLA（2026，arXiv preprint）

该工作解决了音频输入与动作生成缺乏明确联系的问题。将声音特征加入模型后，策略仍可能依赖视觉或固定动作模式，不能保证它真正根据声音选择目标、等待事件或主动探测。

系统基于 GR00T N1.7，将语义声音嵌入和波形声学线索组成因果历史，通过音频 token 与特征调制影响连续动作生成。训练时加入声音—动作绑定目标，在匹配的非音频上下文中监督声音差异与动作差异的关系。论文构建了包含八项任务、960 条示范的 LIBERO-Audio，并采用音频交换实验检查声音对预测的影响。

它的主要创新是显式约束声音与动作之间的对应关系，并覆盖摇晃盒子、触发后关闭蜂鸣器等主动感知任务。原文表 II 报告平均成功率为 66.25%，表 III 中去掉绑定目标后为 38.25%；但两项主动探测任务分别只有 32% 和 20%。局限是主动感知仍不稳定，音频影响动作也不等于影响必然正确；本次访问匿名代码入口返回 401，资源可得性待核实。

[论文][listenvla] · [作者提供的代码入口][listenvla-code]。依据 v1 §III-D、§IV 与表 II–III。

## 7. RoboOmni: Proactive Robot Manipulation in Omni-modal Context（2025，arXiv preprint）

该工作解决了机器人依赖明确指令、难以从日常交互中推断用户意图的问题。真实场景中的任务需求可能体现在多人对话、非语言声音和视觉上下文中，而不是一句完整命令。

系统采用 Perceiver–Thinker–Talker–Executor 架构，将多模态感知、意图推理、交互确认、语音与动作输出结合。论文构建约 14 万条 episode 的 OmniAction，通过改写已有轨迹指令、语音合成、多说话人混音、事件声插入和背景混音生成上下文，并在仿真和真实场景中评估。

它的主要创新是将上下文意图理解与机器人操作连接，使模型能够利用语音之外的环境声音。局限是数据主要经过合成增强，不能将其规模解释为真实接触音频示范数量；意图推断能力与接触动力学感知也需要分别评估。

[论文][roboomni] · [代码与模型说明][roboomni-code] · [OmniAction][omniaction]。依据 v3 §3–4、实验与官方 README。

## 8. From Instruction to Event: Sound-Triggered Mobile Manipulation（2026，arXiv preprint）

该工作解决了移动操作机器人依赖文本指令、难以主动响应环境声音的问题。例如设备发出提示音后，机器人需要判断事件、定位目标，再执行相应交互。

系统提出 Sound-Triggered Mobile Manipulation（STMM），通过 Habitat-Echo 将声学渲染、视觉观测与物理交互结合。高层任务规划器根据声音事件生成技能链，低层策略依次执行导航与操作。论文构建 STMM-12K，包含约 11.86k 个单事件和多事件 episode。

它的主要创新是将声音事件作为移动操作的任务触发来源，评估从事件理解到技能执行的完整链路。局限是实验基于仿真和分层技能，尚不能等同于真实机械臂的通用声音条件策略；原文说明代码和数据将在接收后发布，本次未核实可下载资源。

[论文][stmm]。依据 v3 §3–6。

## 9. MuSTMM: Learning Sound-Triggered Mobile Manipulation across Multiple Scenes（2026，arXiv preprint）

该工作进一步研究声音触发移动操作在未见场景中的泛化。仅改变同一场景内的物体布局，难以判断策略是否能够适应新的建筑结构和导航约束。

系统将任务扩展到 31 个场景，提供预计算的双耳房间脉冲响应和场景隔离的数据划分。导航策略将深度观测积累为空间记忆，并投影为鸟瞰占据图，再与声音上下文融合，为后续导航和操作提供目标位置与场景结构信息。

它的主要创新是把跨场景评测与显式空间记忆引入声音触发操作。局限是声音渲染和操作仍依赖仿真平台，真实空间声学迁移需要额外验证；原文仍写接收后发布代码和数据，本次未核实下载状态。

[论文][mustmm]。依据 v1 的数据、方法和实验部分。

## 10. MuseVLA: An Adaptive Multimodal Sensing Vision-Language-Action Model for Robotic Manipulation（2026，arXiv preprint）

该工作解决了 VLA 难以利用温度、声音和雷达等异构测量的问题。不同任务需要的感知信息不同，将所有传感器固定接入同一输入结构，会增加采集和适配成本。

系统将传感器视为按需调用的工具。模型根据指令和视觉上下文选择传感器及目标，将测量转换为与 RGB 对齐的 grounded sensor image，再用于动作生成。声音任务主要使用麦克风阵列生成声学热图，支持根据声音寻找目标物体。

它的主要创新是用统一的图像中间表示连接不同传感器与 VLA，便于复用已有视觉处理结构。局限是声学热图侧重声源空间信息，与保留波形细节的接触音频输入不同，不能直接据此推断精细接触动力学能力。

[论文][musevla] · [代码与数据说明][musevla-code]。依据 v2 与官方 README。

## 11. PolyUMI: Accessible Visual-Tactile-Audio Data Collection for Object Inference and Manipulation（2026，arXiv preprint）

该工作解决了视觉、触觉与接触声音难以同步采集和用于操作学习的问题。隐藏物体识别和滑移控制需要互补的传感器反馈，仅依赖腕部相机可能遗漏关键接触变化。

系统采用手持采集平台记录视觉、触觉与接触音频，再利用多模态示范学习物体推断和操作策略。论文评估了隐藏物体识别与闭环滑移控制，并通过传感器组合消融分析不同输入的作用。

它的主要创新是将多种接触相关传感器整合到可用于示范采集的平台中，为多模态操作研究提供硬件与数据路径。局限是不同任务依赖不同传感器组合，完整系统的提升不能全部归因于声音，迁移到新夹爪也需要重新核对安装和同步方式。

[论文][polyumi] · [项目与硬件代码][polyumi-project]。依据 v2 的系统与实验部分。

## 12. S2A2: Audio-Visual Imitation Learning for Manipulation Tasks Using Acoustic Spatial Information（2026，arXiv preprint）

该工作解决了机器人仅凭视觉或声音类别难以选择正确发声目标的问题。当多个物体同时存在时，声音的空间来源与频谱内容需要共同参与判断。

系统提出 Spatial-Spectral Audio Action（S2A2），将视觉特征、声学空间信息和声音内容特征结合，用于模仿学习中的目标选择和操作。论文设计了需要声源定位、声音识别与主动探索的操作任务。

它的主要创新是将声学空间线索引入音视动作学习，补充仅使用声音语义特征的策略。局限是其主要验证范围为音视模仿操作，不能直接归类为通用语言条件 VLA，真实多声源和新环境泛化仍需结合具体实验判断。

[论文][s2a2]。依据 v2 的方法与实验部分。

## 13. Learning Robot Manipulation from Audio World Models（2025，arXiv preprint）

该工作解决了仅感知当前声音不足以支持提前决策的问题。注水等任务的视觉变化可能不明显，但声音的音高和时间演化能够反映过程状态，预测未来声音有助于提前调整动作。

系统先将音频转换为频谱并学习潜空间，再通过流匹配模型生成未来声音表示。动作策略以当前图像、当前声音与预测声音为条件生成控制量，声音模型与策略分阶段训练。论文在真实 Kinova Gen3 上通过按压和松开饮水机按钮控制注水，并在仿真钢琴任务中使用未来音乐信息辅助策略。

它的主要创新是将声音未来预测接入机器人动作学习，提供了音频世界模型辅助操作的直接例子。原文 §3.1 报告注水任务 30 次测试全部成功。局限是预测主要由历史音频驱动，未展示通用的候选控制动作条件反事实推演；实验也不足以证明跨容器、跨流速和跨机器人泛化，本次未定位到已核实的官方代码和数据入口。

[论文][audio-wm]。依据 v1 §2–3。

## 14. Audio-Visual World Models: Learning Physically Grounded Multisensory Dynamics（2025，arXiv preprint）

该工作解决了世界模型主要预测视觉、缺少动作条件声学变化建模的问题。机器人移动后，视觉内容、声源方向和声音传播都会改变，需要同步预测才能支持空间推理。

系统提出 AV-CDiT，将历史视觉、双耳声音、动作和时间条件联合输入，预测未来视觉与声音，并用于连续视听导航。论文基于 Matterport3D 和 SoundSpaces 2.0 构建 AVW-4k，包含约 30 小时、76 个室内环境和 4,500 条轨迹。

它的主要创新是将视听动态放入动作条件世界模型，支持不同移动动作后果的预测。局限是这里的动作和物理变化主要对应导航、视点与声场，不是机械臂接触动力学；本次未定位到已核实的官方代码和数据下载入口。

[论文][avwm]。首次公开于 2025 年，本文依据 2026-08-04 的 v4，重点参考 Formulation and Dataset、Methodology 与实验部分。

## 15. Dreaming the Sound of Contact: Leveraging Video and Audio Generation for Zero-Shot Force-Aware Manipulation and Data Generation（2026，arXiv preprint）

该工作解决了从生成视频提取机器人轨迹时缺少接触力信息的问题。仅恢复运动几何可能不足以完成接触丰富的任务，执行过程中还需要适当的力变化。

系统联合利用生成的视频和接触声音，从视频导出运动轨迹，并根据生成声音的响度塑造目标力曲线，再通过 Franka 的闭环力调节器执行。论文还将该流程用于生成数据，训练能够闭环完成任务的策略。

它的主要创新是让声音生成参与接触控制与机器人数据生成。局限是声音响度与接触力之间的映射依赖任务、材料和传感条件，不能作为通用力学规律；实际力控制仍依赖力反馈，与直接根据当前麦克风输入生成动作的设置不同。

[论文][dream-contact] · [项目与数据入口][dream-contact-project]。依据 v2 的方法与真实机器人实验，未完整下载数据。

## 16. AudioWorldSim: Realistic Binaural Audio Datasets For World Models（2026，arXiv preprint）

该工作解决了声音世界模型缺少连续、可控的双耳交互数据的问题。静态声音片段难以体现机器人移动与声学观测变化之间的关系。

系统在 SoundSpaces 2.0 上扩展自动导航轨迹采集，记录连续双耳声音及环境交互相关信息，并修正连续声音组合中的问题。研究者可以通过平台生成用于空间听觉和音频动态建模的数据。

它的主要创新是提供面向音频世界模型的数据生成工具。局限是其本身是仿真与采集基础设施，不是已经训练完成的通用机器人策略，导航声场数据也不能直接替代真实接触操作数据。

[论文][audio-world-sim] · [代码][audio-world-sim-code]。依据 v1；声学仿真背景见 [SoundSpaces 2.0][soundspaces]。

## 17. BinauralVAE: Spatial Audio Reconstruction For World Models（2026，arXiv preprint）

该工作解决了双耳声音缺少适合世界模型使用的潜在表示的问题。音频压缩不仅需要保留声音内容，还需要尽量保留与方向和空间关系有关的双耳差异。

系统研究多种变分自编码器，包括复数表示相关结构，对仿真导航过程中采集的双耳信号进行编码和重建，并与 AudioWorldSim 的数据生成流程配合。

它的主要创新是为音频世界模型提供空间声音表示与重建基线。局限是重建质量不等于未来预测能力，VAE 本身没有证明已经学会动作导致的状态变化，也没有直接给出闭环控制收益；完整声音世界模型仍是后续目标。

[论文][binaural-vae] · [代码入口][binaural-vae-code]。依据 v1 的表示学习与重建实验。

## 18. RH20T: A Comprehensive Robotic Dataset for Learning Diverse Skills in One-Shot（2023，arXiv preprint）

该工作解决了真实机器人技能学习缺少多模态、接触丰富示范数据的问题。仅有视觉与动作轨迹，难以研究接触状态、物理反馈与跨传感器学习。

数据采集系统同步记录多视角视觉、力、声音和机器人运动信息，并提供对应的人类示范视频与标定资料。官方项目介绍了超过 110,000 条真实机器人操作序列，并提供数据下载和 API。

它的主要贡献是建立真实多传感器操作数据资源，适合研究声音与动作对齐、多模态状态估计和示范迁移。局限是需要逐子集核对音轨、时间戳和动作接口；RH20T-C 与 RH20T-NC 的许可不同，不能将整套数据视为具有统一的商业使用许可。

[论文][rh20t] · [项目与数据][rh20t-project] · [API][rh20t-api]。依据 v2 摘要与官方模态、规模和许可说明，未检查全量音轨。

## 19. Audio-Language-Action Models with Direct Speech Conditioning for Robotic Manipulation（2026，Late Breaking Results）

该工作解决了语音识别后再输入 VLA 所带来的延迟和转写误差传播问题。传统流水线需要先把声音变成文本，再由动作模型处理指令。

系统提出 Speech-π₀.₅，在 π₀.₅ 上通过跨模态投影将语音特征转换为音频 token，直接参与动作生成，并采用分离的音频与任务适配模块进行训练。论文围绕语音条件操作、响应延迟和口音变化开展评估。

它的主要创新是减少语音到动作之间对显式文本转写的依赖。局限是原文为短篇 Late Breaking Results，主要验证语音指令处理，不能据此推断模型已经能够理解接触声音或预测物理状态。

[论文][speech-action]。依据 arXiv v1；完整标题含 Late Breaking Results 前缀。

## 20. VoiceGuard: An Audio-Native LLM-VLA Pipeline for Wheelchair-Mounted Assistive Manipulation（2026，arXiv preprint）

该工作解决了辅助机械臂语音交互中的指令歧义、非指向性对话和执行中断问题。机器人除了理解用户需求，还需要区分有效请求与背景交谈。

系统使用本地唤醒与停止检测、音频原生语言模型和结构化请求校验，将通过检查的任务交给 SmolVLA 执行。语音理解、请求确认和机器人动作分别由相应模块承担。

它的主要创新是将灵活语音输入与受约束的动作执行结合，形成辅助操作流水线。局限是它主要研究语音接口和执行编排，不是接触声音感知模型或音频世界模型，初步实验也不能代表开放环境中的通用操作能力。

[论文][voiceguard]。依据 v1 的系统与初步实验。

## 21. 相关数据集对比

| 数据集或基准 | 声音来源与同步信息 | 动作监督 | 适用研究 | 资源状态与局限 |
| --- | --- | --- | --- | --- |
| [RH20T][rh20t-project] | 真实视觉、声音、力和机器人状态 | 真实机器人动作 | 接触反馈、音频动作对齐、多模态学习 | 官方提供下载和 API；需核对子集音轨与许可 |
| [ManiWAV][maniwav-code] | 真实接触音频和视觉 | UMI 操作轨迹 | 接触操作模仿学习 | 官方代码有数据入口；需处理人手到机器人的传感差异 |
| [FuSe][fuse-data] | 真实异构传感器数据 | 机器人动作与语言相关监督 | 预训练策略的传感器适配 | 官方列有数据与模型；并非每条轨迹都包含音频 |
| [OmniAction][omniaction] | 轨迹视觉配合合成语音、事件声和背景声 | 机器人动作与上下文指令 | 意图理解、情境响应 | 官方列有发布入口；不能作为实录接触声数据使用 |
| [OpenX-Sound][openx-sound] | 所选 OpenX 轨迹配合合成音轨 | 原有动作、语言和本体状态 | 声音与机器人时序对齐预训练 | 官方列有发布入口；声音不是原始实录 |
| HEAR-Bench | 事件条件仿真声音流 | 七项任务及声音因果成功条件 | 瞬态事件响应、等待和过程监控 | 见 [HEAR 原文与代码][hear-code]；需按发布版本检查资源完整性 |
| LIBERO-Audio | 渲染声音、视觉、指令和本体状态 | 八项任务、960 条示范 | 声音选目标、延迟响应、主动探测 | [原文][listenvla]已说明；匿名入口本次返回 401 |
| STMM-12K / MuSTMM | 仿真双耳声音与场景观测 | 导航和操作技能链 | 声音触发移动操作 | [STMM][stmm] 与 [MuSTMM][mustmm] 均写接收后发布，下载待核实 |
| AVW-4k | 仿真同步双耳声音与视觉 | 导航动作及未来观测 | 动作条件视听世界模型 | [原文][avwm]报告约 30 小时、4,500 条轨迹；下载入口未核实 |
| [AudioWorldSim][audio-world-sim-code] | 仿真连续双耳声音与环境观测 | 导航轨迹及相关元数据 | 自建音频动态数据 | 数据生成平台，具体字段依采集配置 |

上述资源按真实采集、合成增强与仿真生成区分。通用声音事件或音视频数据可以用于编码器预训练，但缺少同步机器人控制动作时，不能直接作为 VLA 行为克隆数据。原版 Open X-Embodiment、LIBERO 和 RLBench 也不能直接等同于其音频增强版本。本文未完整下载这些数据，发布入口与可训练数据完整性需要分别核实。

## 22. 研究方向比较

| 研究方向 | 声音的作用 | 代表工作 | 主要局限 |
| --- | --- | --- | --- |
| 接触操作学习 | 提供接触事件和隐藏物理状态 | ManiWAV、FuSe、Audio-VLA | 传感器安装差异、真实声音覆盖与跨任务迁移 |
| 声音事件响应 | 决定目标、触发时机和动作顺序 | HEAR、ListenVLA、STMM | 短促事件遗漏、延迟与主动探测稳定性 |
| 情境意图理解 | 结合语音、环境声和视觉推断任务 | RoboOmni | 合成数据与真实交互差异、意图识别可靠性 |
| 声音未来预测 | 提供过程前瞻和动作后果信息 | Audio World Models、AVWM | 动作条件建模、长期误差与闭环收益验证 |
| 语音指令控制 | 将口头需求转换为动作 | Speech-π₀.₅、VoiceGuard | 与非语言声音感知的能力边界不同 |

现有研究已经覆盖声音条件策略、声音参与的 VLA 和音频世界模型。它们的区别主要在于声音承担的功能：理解指令、识别事件、估计接触状态，或预测未来观测。声音预测还需要区分历史音频续写、训练辅助目标与显式动作条件世界模型，不能仅依据名称判断规划能力。

从后续研究角度看，较具体的问题包括短促声音的时序留存、通过主动交互获取声音证据，以及声音预测相对历史记忆是否提供额外收益。这些是基于文献比较提出的研究判断，仍需在统一数据与计算预算下，通过静音、音频错配、触发延迟和未见环境等对照实验验证。

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
