<div align="center">
  <img src="assets/logo-512.png" width="132" alt="PocketMen with You" />
  <h1>PocketMen with You</h1>
  <p><strong>上传至少两张照片，在本地生成一直陪着你的高清 Codex 萌宠。</strong></p>
  <p><strong>v0.3：Neural Local Studio。默认不依赖 hatch-pet，不需要 OPENAI_API_KEY。</strong></p>
</div>

[English](README.md)

## v0.3 解决了什么

v0.2 的本地引擎很稳定，但本质上只能对已有像素做抠图、缩放、旋转与变形，因此无法真正“想象”照片里没有出现的新姿态。

v0.3 把 Local Engine 升级成了**真正的本地生成式图像引擎**：当机器具备合适的 NVIDIA GPU 时，PocketMen 会使用开放权重、多参考图像编辑模型生成统一的角色母版和九类动作关键姿态，然后再由自己的透明背景处理、微动画、图集组装和 QA 管线完成 Codex Pet。

```text
至少2张参考图
    ↓
Codex 视觉识别并建立 Identity Lock
    ↓
硬件检测
    ↓
Neural Local Studio
    ├─ 默认：FLUX.2 [klein] 4B
    └─ Identity-Max：Qwen-Image-Edit-2511
    ↓
统一母版 + 九类动作关键姿态
    ↓
纯色背景去除 / 透明边缘净化
    ↓
稳定微动画
    ↓
8×9 / 1536×1872 Codex 图集
    ↓
验证、Contact Sheet、GIF
    ↓
pet.json + spritesheet.webp
```

如果本地硬件或依赖不足，会自动退回 v0.2 的确定性引擎，而不是要求用户配置 OpenAI API Key。

## 两套神经引擎

### FLUX.2 [klein] 4B —— 默认推荐

适合大部分用户：

- 支持本地文生图与图像编辑；
- 支持多参考图；
- Apache-2.0；
- 面向消费级 NVIDIA GPU；
- PocketMen 在兼容硬件上自动优先选择。

### Qwen-Image-Edit-2511 —— Identity-Max

用于人物、宠物、多人/多主体等身份一致性要求更高的情况：

- 支持多图编辑；
- 强调人物/角色一致性和新视角编辑；
- Apache-2.0；
- 体量更大，建议高显存设备与 CPU offload。

PocketMen 不把 FLUX.2 [dev] 作为公开项目默认后端，因为其模型许可证为非商业用途许可。

## 三档质量

- `draft`：只生成一个高质量母版，九类动作由本地微动画完成；
- `balanced`：母版 + 各状态关键姿态，质量/速度平衡；
- `max`：九种状态全部独立生成关键姿态，最大化动作自然度。

## 用户实际只需要这样做

上传至少两张图片，然后告诉 Codex：

```text
使用 $pocketmen-with-you 根据这些图片制作并安装一个 Codex 宠物。
我的机器支持时优先使用 Neural Local Studio。
风格：hero-chibi。
主体：person。
质量：max。
严格保持人物身份，不要调用 hatch-pet，也不要要求 OPENAI_API_KEY。
```

Skill 会直接利用 Codex 本身对上传图片的视觉理解，把稳定特征整理为 `identity-notes`，再交给本地生成引擎。

## 本地命令

检测硬件：

```bash
pocketmen doctor
```

自动选择：

```bash
pocketmen create \
  --reference photo-1.jpg \
  --reference photo-2.jpg \
  --name "小黑" \
  --subject-type animal \
  --style soft-real \
  --engine auto \
  --quality balanced \
  --output ./pocketmen-output \
  --install
```

最高质量默认模型：

```bash
pocketmen create ... --engine neural --backend flux2-klein-4b --quality max
```

身份一致性优先：

```bash
pocketmen create ... --engine neural --backend qwen-image-edit-2511 --quality max
```

## 一键安装

```text
INSTALL_SKILL.bat
```

安装器会把 Skill 放入 `~/.agents/skills/pocketmen-with-you`，并创建独立虚拟环境；Windows 上还会检测 NVIDIA 显存，兼容机器会自动安装 Neural Local Studio 依赖。

希望提前下载并缓存默认模型时：

```text
PREPARE_NEURAL_ENGINE.bat
```

Identity-Max：

```text
PREPARE_IDENTITY_MAX.bat
```

模型权重保存在正常 Hugging Face 缓存中，不会被塞进 GitHub 仓库。

## “无限接近 ImageGen”应该怎样理解

v0.3 的目标不是声称某个开放权重模型在所有任务上等于闭源前沿模型，而是针对 **“2+张照片 → 统一身份 → 九类萌宠动作 → Codex 图集”** 这一窄任务把差距尽量压小：

- 多参考身份锚定；
- 独立动作关键姿态生成；
- 统一风格母版；
- 强约束提示词；
- 固定背景与本地透明化；
- 微动画稳定器；
- 严格图集 QA。

因此，人物挥手、真实奔跑、动物抬爪、跳跃、Q版重绘、主人+宠物等以前无法靠简单变形完成的动作，现在能由本地模型真正生成。对于复杂世界知识、文字渲染和极复杂多物体场景，和 GPT Image 2 仍可能存在差距。

## 隐私

原始私人照片默认只在本机处理，不会被自动提交到 GitHub 或 Release。最终 Codex 安装包只包含 `pet.json` 和 `spritesheet.webp`。

## License

PocketMen 本身采用 MIT；可选模型保持各自许可证，项目只引用、不再分发模型权重。
