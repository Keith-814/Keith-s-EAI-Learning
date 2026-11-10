---
layout: post
title: "文献调研进度"
date: 2026-11-10
author: Keith
categories: blog
toc: true
---

# 文献调研进度汇报

这组文献的主线可以概括为：先解决机器人如何生成连续、精细且多模态的动作（Diffusion Policy、FAST、ACT），再发展视觉语言动作模型的通用控制能力（RT-1、RT-2、OpenVLA、π₀、π₀.₅），最后进一步关注长时序规划、环境预测和零样本执行（Reflective Planning、V-JEPA 2、World Action Models）。

## 1. π₀.₅: a Vision-Language-Action Model with Open-World Generalization

该工作解决了视觉语言动作模型在陌生物体、陌生环境和新任务上的泛化能力不足问题。方法上，它在 π₀ 的流匹配动作生成基础上，引入高层语义或子目标规划与低层连续控制，并混合互联网视觉语言数据和多机器人数据进行训练，从而提升开放世界泛化能力。

## 2. π₀: A Vision-Language-Action Flow Model for General Robot Control

该工作解决了不同机器人、不同任务之间控制策略难以统一的问题。它采用预训练视觉语言模型结合动作专家模块的结构，通过流匹配直接生成连续动作序列，并利用多种机器人数据进行联合训练，实现通用机器人控制。

## 3. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

该工作针对机器人动作具有多峰分布、精细操作难以建模的问题，提出将动作序列建模为条件扩散过程。策略根据当前视觉观测，通过逐步去噪生成一段未来动作，再采用滚动执行方式完成操作，因此能够处理复杂且不确定的动作分布。

## 4. FAST: Efficient Action Tokenization for Vision-Language-Action Models

该工作解决了视觉语言动作模型中连续动作离散化后序列过长、推理效率低的问题。它先将动作序列转换到频域，再进行量化和压缩编码，把一段连续动作表示为较少的离散 token，从而降低训练和推理成本。

## 5. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

该工作解决了双臂精细操作数据采集成本高、硬件难以普及的问题。作者搭建了低成本的 ALOHA 双臂遥操作平台，并使用 ACT 动作分块模型和时间集成方法，从少量示范中学习精细的双臂协同操作。

## 6. OpenVLA: An Open-Source Vision-Language-Action Model

该工作解决了视觉语言动作模型难以复现、难以扩展和缺少开源基线的问题。它基于预训练视觉语言模型，在大规模机器人示范数据上进行微调，将机器人动作离散成 token 进行预测，并公开模型、训练方法和代码，支持多种机器人任务。

## 7. Reflective Planning: Vision-Language Models for Multi-Stage Long-Horizon Robotic Manipulation

该工作解决了长时序、多阶段机器人任务中计划容易出错且错误会持续累积的问题。它利用视觉语言模型生成任务计划，并在执行后根据视觉反馈进行反思、错误诊断和局部重新规划，从而提高复杂任务的成功率。

## 8. RT-1: Robotics Transformer for Real-World Control at Scale

该工作解决了机器人策略难以随着任务数量和数据规模扩大而保持稳定性能的问题。它使用视觉编码器和 Transformer，将图像、语言指令及历史观测输入模型，并输出离散化的机器人动作，通过大规模真实机器人数据训练得到通用控制策略。

## 9. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control

该工作解决了视觉语言模型中的互联网知识难以迁移到机器人控制的问题。它将机器人动作表示为语言 token，并把视觉语言模型的网页知识与机器人轨迹联合微调，使模型能够根据语义知识进行物体识别、抽象推理和零样本操作。

## 10. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

该工作解决了世界模型依赖人工标注、难以同时支持视频理解、未来预测和机器人规划的问题。它通过自监督学习在视频数据上预测未来的潜在表示，而不是直接预测像素，并进一步结合动作信息进行环境预测和模型预测控制。

## 11. World Action Models are Zero-shot Policies

该工作研究如何直接利用世界模型完成机器人决策，减少针对每个任务单独训练策略的需求。其方法是让模型预测不同候选动作导致的未来状态，再根据目标达成程度对动作进行评估和选择，从而通过规划实现零样本策略执行。

## 12. ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation

该工作解决了自然语言指令难以转化为精确、可执行的多阶段机器人操作约束的问题。它用物体上的三维语义关键点表示操作对象，结合视觉基础模型和视觉语言模型，自动生成描述关键点空间关系的子目标约束与路径约束，再通过分层优化求解目标位姿和运动轨迹，并根据视觉反馈持续更新，实现对新物体和环境变化的泛化。
