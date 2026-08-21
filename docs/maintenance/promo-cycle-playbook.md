# PocketMen 长期运营执行手册（24h 评论 + 三社区模板 + 周期报表）

本文件用于配合 `.github/workflows/pocketmen-auto-ops.yml` 的自动 issue 节奏：

- 每天 24h 评论更新 Issue
- 周一：例行维护 + 周期报表 Issue
- 周四：社区宣发推进 Issue

## 1) 24h 评论更新执行法

每天工作项会在 GitHub 自动创建。请在 24h 内完成：

1. 在讨论区更新一条参数实验评论
2. 在至少一条核心贴内补充 1 组对比结果
3. 回复 1~2 个用户反馈
4. 将三社区发布链接回填到本条 issue

### 统一参数模板

```text
模型：FLUX.2-klein-4B（默认）
身份增强：Qwen-Image-Edit-2511（可选）
steps: 28
cfg: 1.5
seed: 42
negative_prompt: blurry, distortion, artifact, jitter
```

## 2) 多社区同步模板（固定可用）

### 知乎模板
```text
今天同步一条 24h 跟进，重点是参数复现和效果对比：
- 默认后端：FLUX.2-klein-4B
- 可选后端：Qwen-Image-Edit-2511
- 参数：seed=42, cfg=1.5, steps=28

补充 1~2 张对比图，欢迎评论需求参数组合和问题反馈。
```

### V2EX 模板
```text
PocketMen with you 24h 跟进

本次更新：
- 参数：seed/CFG/steps
- 对比：同一提示词多后端对比（FLUX.2-klein-4B vs 可选后端）
- 特点：正常生成路径无需 OPENAI_API_KEY，支持离线兜底
```

### Reddit 模板（r/LocalLLaMA / r/MachineLearning）
```text
PocketMen-with-you open-source local pet animation update (24h follow-up)

- Default backend: black-forest-labs/FLUX.2-klein-4B
- Optional Identity-Max: Qwen/Qwen-Image-Edit-2511
- Parameter block:
  steps=28, cfg=1.5, seed=42
- Normal generation does not require OPENAI_API_KEY
```

## 3) 周期报表填写规范

周一 issue 会自动带入以下字段：

- Stars / Forks
- Open Issues / Open PRs
- 24h 与 7d 新增 Issue/PR
- CI 最近状态

请补充：

- 24h 评论更新完成率
- 三社区发帖链接
- 用户反馈回复耗时
- 下周 3 项优先级

## 4) 推荐执行频率

### 每日
- 完成 24h 评论更新 issue

### 周一
- 处理例行维护 + 填写周期报表

### 周四
- 做 72h 社区宣发推进并同步三平台

## 5) 发布前检查

发布/同步前确认：

- README 示例与仓库当前版本一致
- 禁止上传敏感私有图片
- 确认链接无重复/404
- 保持口径一致（参数、模型、版本）
