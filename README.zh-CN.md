<div align="center">
  <img src="assets/logo-512.png" width="132" alt="PocketMen with You 原创红黄陪伴胶囊标志" />
  <h1>PocketMen with You</h1>
  <p><strong>只需上传至少两张参考图，就把重要的人、宠物或原创幻想生物做成一直陪着你的 Codex 高清萌宠。</strong></p>
</div>

[English](README.md)

## 项目定位

PocketMen with You 是一个面向 Codex 的 **Skill-first** 开源项目。它不把“生成一张可爱图片”当作终点，而是把参考图识别、身份特征锁定、九类动作生成、透明图集封装、动态预览、视觉 QA 与本地安装组成一条可复用工作流。

适合四类常用风格：

- `hero-chibi`：帅气又 Q 弹的卡通人物；
- `soft-real`：尽量忠实还原毛色、眼睛、体型和项圈的小动物；
- `plush`：柔软玩偶/吉祥物；
- `capsule-creature`：原创幻想生物 + 项目自有红黄陪伴胶囊；
- `auto`：自动选择。

## 三步使用

1. 在 Codex 中打开本仓库；
2. 上传 **至少两张图片**；
3. 输入：

```text
使用 $pocketmen-with-you，根据我上传的参考图生成一只 Codex 陪伴宠物。
风格 auto，尽量忠实保持身份特征，通过视觉 QA 后自动安装。
```

仓库自带 `.agents/skills/pocketmen-with-you`，Codex 会从仓库级 skill 路径发现它。

## 为什么至少两张图

单张图很容易把偶然的姿态、光照、遮挡或表情当成固定特征。PocketMen 要求至少两张，是为了先抽取跨图片稳定的身份锚点：人物的发型与脸部轮廓、猫狗的毛色与眼睛、固定配饰、体态、主色和气质，再把这些锚点带进九类动作。

## Codex 宠物图集

项目验证：8 列 × 9 行、单格 192 × 208 px、最终 1536 × 1872 px，九行依次为 `idle / running-right / running-left / waving / jumping / failed / waiting / running / review`。未使用单元格必须完全透明。

## 关于精灵球视觉

为了让项目具有“口袋伙伴/捕捉陪伴”的记忆点，本项目使用**原创红黄陪伴胶囊**：采用红黄斜向分区、深色斜带和爱心/伙伴核心图形，刻意避免复制现有商业角色或精灵球的具体商标外观。

## 发布到 GitHub

本包已预设目标账户 `six-nut` 与仓库 `PocketMen-with-you`。Windows 双击：

```text
PUBLISH_GITHUB.bat
```

脚本会先检查 `gh auth status`，确认当前 GitHub CLI 登录的是 `six-nut`，再创建公开仓库、推送 `main`、写入 Topics 与标签。不会读取或打印 GitHub Token。

发布后，建议把 `assets/social-preview.png` 手动上传为 GitHub Social preview。

## 许可

MIT。项目与 Nintendo、The Pokémon Company、Game Freak、OpenAI、GitHub 均无从属或官方关联。
