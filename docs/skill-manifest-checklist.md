# PocketMen-with-you 可安装 Codex Skill 清单评估（轻量）

目标：先确认是否值得以“可安装 Skill 包”发布，而不改变现有本地优先流程。

## 0. 结论位（先填）
- 结论（PASS / BLOCK / DEFER）：
- 决策时间窗：2026-09-07（更新）
- 负责人：`six-nut`

## 1. 结构与清单
- [ ] 明确 Skill 包入口（命令/接口）：CLI 与 `skill.json` 约定是否已统一。
- [ ] 包内是否只保留可执行内容（无测试镜像、无私有参考图、无本地临时目录）。
- [ ] 与现有运行目录分离：`scripts/` 与打包文件不互相污染。
- [ ] 产物最小化：`pet.json` + `spritesheet.webp` + 必要运行文档。

## 2. 隐私与安全边界（必须通过）
- [ ] 不在包内持久化用户参考图、prompt 日志或凭证。
- [ ] 安装/卸载不触发外部网络请求（除明确配置）。
- [ ] 安装路径校验禁止路径穿越，失败场景可回滚。
- [ ] 输出不含 secret、token、原始 HTTP 头等敏感字段。

## 3. 兼容性与回退能力
- [ ] 兼容当前 `openai` 无需场景（默认保持 `api_key_required=false`）。
- [ ] 兼容既有离线 fallback（无 GPU 时仍可生成可安装包）。
- [ ] 包内依赖与模型加载遵循版本锁定策略，支持无网络回退到确定性模式。
- [ ] 与现有发布流程兼容（`pypi`、Release notes、`run-summary`）。

## 4. 维护与回归
- [ ] 安装前后执行 `validate` 与 `atlas` QA。
- [ ] 增加打包链路验证脚本（至少 1 条自动化检查）。
- [ ] 更新 `README`，说明安装/卸载和升级方式。
- [ ] 增加周更发布风险记录（Issue/PR 责任人）。

## 5. 下一步任务拆解（如通过）
- [ ] 在 `scripts/` 输出 `skill-manifest`/`skill-entry` 模板。
- [ ] 增加 `skill` 打包命令（dry-run + 实际打包）。
- [ ] 增加安装后自检（验证 `pet.json` + `spritesheet.webp`）。
- [ ] 形成一条独立 PR：`chore: add codex skill manifest + install path`。
