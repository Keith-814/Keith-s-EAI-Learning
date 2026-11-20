---
layout: post
title: "声音驱动机器人文献调研"
date: 2026-11-20
author: Keith
categories: research
tags: [声音感知, Audio-VLA, VSLA, 世界模型, 多模态数据集, 文献调研]
toc: true
excerpt: "选取声音驱动操作、VLA、世界模型与数据集的八篇重点文献，介绍各自解决的问题、主要亮点和主框架。"
---

声音可以补充视觉难以判断的接触状态，也能作为环境事件的触发信号，帮助机器人决定做什么、何时行动。本文选取八篇重点文献，涵盖声音驱动操作、视觉声音语言动作模型、音频世界模型及相关数据集，重点说明每篇解决的问题、亮点和主框架。

## 1. ManiWAV: Learning Robot Manipulation from In-the-Wild Audio-Visual Data（2024，arXiv preprint）

**解决的问题：** 视觉难以完整反映擦拭、翻动物体等操作中的接触状态，而传统机器人遥操作又限制了带声音示范的采集范围。

**亮点：** 在 UMI 手持设备中加入接触麦克风，让人类直接在不同环境中采集声音与动作示范，再迁移到机器人执行。论文验证了擦拭、翻贝果、倒出物体和魔术贴捆线等任务，提供了接触音频参与操作学习的完整方案。

**主框架：** 手持设备同步采集图像、接触声音与操作轨迹 → 视觉编码器和音频编码器提取特征 → 多模态融合 → 扩散策略生成动作序列 → 机器人执行并根据新观测滚动更新。

[论文][maniwav] · [项目][maniwav-project] · [代码与数据][maniwav-code]。依据 v2 的方法与实验。

## 2. Audio-VLA: Adding Contact Audio Perception to Vision-Language-Action Model for Robotic Manipulation（2025，arXiv preprint）

**解决的问题：** VLA 主要依赖视觉与语言，对碰撞、接触变化和操作完成过程的反馈感知不足，容易遗漏图像中不明显的动态信息。

**亮点：** 将接触声音直接引入 VLA，使动作决策能够使用交互过程中的声学反馈；同时在 LIBERO、RLBench 中增加碰撞相关声音，并提出 Task Completion Rate（TCR）评价过程完成情况。

**主框架：** 图像经 DINOv2、SigLIP 编码，声音经 AudioCLIP 编码 → 多模态投影对齐 → 与语言共同输入 Llama2 主干 → 通过 LoRA 微调学习动作输出 → 执行后持续接收视觉与声音反馈。

[论文][audio-vla]。依据 v1 §III–IV。

## 3. Towards the Vision-Sound-Language-Action Paradigm: The HEAR Framework for Sound-Centric Manipulation（2026，arXiv preprint）

**解决的问题：** 提示音、碰撞声等短促信号可能在动作块执行期间出现并消失，机器人下一次更新策略时已经无法听到，导致漏响应或动作时机错误。

**亮点：** 显式研究动作执行间隔中的声音遗漏，将声音记忆、时间对齐和动作生成结合。配套 OpenX-Sound 用于音频增强预训练，HEAR-Bench 检查机器人是否在相关声音发生后才正确行动。

**主框架：** 视觉、流式声音、语言与本体状态输入 → Historizer 持续保存声音事件 → Envisioner 推理任务与阶段 → Realizer 通过流匹配生成动作块。训练时增加 Advancer 预测近未来声音 token，部署时移除该预测模块。

[论文][hear] · [项目][hear-project] · [代码][hear-code] · [OpenX-Sound][openx-sound]。依据 v2 §3–6；OpenX-Sound 的声音为合成增强。

## 4. Listen Before Act: Audio-Conditioned Robot Manipulation with ListenVLA（2026，arXiv preprint）

**解决的问题：** 给 VLA 加入音频输入后，模型仍可能只依赖视觉或固定动作模式，缺少对声音变化与动作变化之间关系的明确学习。

**亮点：** 引入声音—动作绑定目标，在视觉、指令与机器人状态匹配的条件下，监督不同声音对应的动作差异。任务覆盖发声目标选择、延迟闹钟，以及先摇晃盒子或触发蜂鸣器再判断的主动感知。

**主框架：** 历史声音 → 语义声音特征与波形声学线索 → 音频 token 和特征调制接入 GR00T N1.7 → 结合视觉、语言与本体状态生成连续动作。训练联合使用动作监督与声音—动作绑定目标，并通过音频交换实验检查声音是否影响动作。

[论文][listenvla]。依据 v1 §III–IV；配套 LIBERO-Audio 包含八项任务、960 条示范。

## 5. RoboOmni: Proactive Robot Manipulation in Omni-modal Context（2025，arXiv preprint）

**解决的问题：** 机器人通常等待明确指令，难以根据多人对话、环境声音和视觉上下文推断用户当前需要的操作。

**亮点：** 将声音与视觉用于情境意图理解，连接主动任务推断、交互确认和动作执行；构建约 14 万条 episode 的 OmniAction，为声音上下文到动作提供训练资源。其音频主要由语音合成、事件声插入与背景混音构成。

**主框架：** Perceiver 编码视觉、语音和环境声音 → Thinker 推断意图与任务 → Talker 生成语音回应或确认，Executor 输出机器人动作 → 根据后续交互更新任务与执行。

[论文][roboomni] · [代码][roboomni-code] · [OmniAction 数据][omniaction]。依据 v3 §3–4 与实验。

## 6. Learning Robot Manipulation from Audio World Models（2025，arXiv preprint）

**解决的问题：** 只利用当前声音难以提前判断操作过程的发展，例如根据注水声音变化决定何时停止，需要对未来声音进行预测。

**亮点：** 将声音未来预测接入动作策略，让机器人利用预测结果提前准备或停止动作。论文在真实机器人注水和仿真钢琴任务中验证；声音预测以历史音频为条件，主要用于特定过程的前瞻。

**主框架：** 历史音频转换为频谱 → 编码到声音潜空间 → 流匹配模型生成未来声音 → 当前图像、当前声音与预测声音共同输入动作策略 → 输出机器人控制量。声音模型与策略分阶段训练。

[论文][audio-wm]。依据 v1 §2–3。

## 7. Audio-Visual World Models: Learning Physically Grounded Multisensory Dynamics（2025，arXiv preprint）

**解决的问题：** 视觉世界模型缺少对声音变化的预测，难以同时描述机器人移动后看到什么、听到什么，以及声源方向和声场如何改变。

**亮点：** 显式以动作为条件联合预测视觉与双耳声音，用于视听导航；构建 AVW-4k，提供约 30 小时、76 个室内环境、4,500 条带动作标注的仿真轨迹。其动作条件建模针对导航与声场变化。

**主框架：** 历史图像与双耳声音分别编码 → 输入动作与时间条件 → AV-CDiT 联合预测未来视觉、音频潜在表示 → 解码未来观测 → 辅助连续视听导航。

[论文][avwm]。首次公开于 2025 年，依据 2026 年修订的 v4，重点参考数据、方法与实验部分。

## 8. RH20T: A Comprehensive Robotic Dataset for Learning Diverse Skills in One-Shot（2023，arXiv preprint）

**解决的问题：** 机器人操作学习缺少同时包含真实声音、接触反馈和动作的多模态数据，难以研究声音与动作对齐及复杂接触技能。

**亮点：** 官方报告采集超过 110,000 条真实机器人操作序列，包含视觉、声音、力和运动信息，并提供对应人类示范视频、标定资料与 API，可作为声音参与机器人学习的数据基础。

**主框架：** 多视角相机、麦克风、力传感器与机器人状态同步采集 → 标定并整理为操作序列 → 通过数据加载与处理接口提供多模态示范 → 支持模仿学习和跨模态研究。使用时需逐子集核对音轨、时间戳与许可。

[论文][rh20t] · [项目与数据][rh20t-project] · [API][rh20t-api]。依据 v2 摘要与官方说明，未检查全量数据。

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
