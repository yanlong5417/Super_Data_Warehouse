# AI 动漫制作

创建时间: 2026-07-12
标签: #AI #动漫 #动画 #创作工具

> 使用 AI 辅助动漫制作的全景概览：从角色设计到完整动画短片。

---

## 一、工具分类

### 角色 / 画面生成 (Image Generation)

| 工具 | 特点 | 访问 |
|------|------|------|
| **NovelAI** | 二次元专精，上手简单，支持 tag 描述 | novelai.net（付费） |
| **Niji Journey** | Midjourney 二次元模型，画风精美 | midjourney.com（付费） |
| **Stable Diffusion** | 开源，可本地部署，LoRA/ControlNet | 免费（需显卡） |
| **哩布哩布 LiblibAI** | 国内 SD 模型站，在线跑图 | liblibai.com（部分免费） |
| **SeaArt** | 国内 AI 绘画平台，模型多 | seaart.ai（免费额度） |
| **千象** | 阿里系 AI 绘画 | qianxiang.aliyun.com |

### 线稿 / 草图 (Sketch to Image)

| 工具 | 用途 |
|------|------|
| **Paints Undo** | 从成品图反推绘画过程，学习画风 |
| **Lineart Converter** | ControlNet lineart 模型，线稿上色/细化 |
| **Krita + AI 插件** | 开源绘画软件 + SD 插件，边画边生成 |

### 动画制作 (Animation)

| 工具 | 说明 |
|------|------|
| **AnimateDiff** | SD 动画工具，生成 GIF/短视频 |
| **Runway Gen-3** | 文生视频 / 图生视频，画风可控 |
| **Pika Labs** | 动画风格视频生成 |
| **ComfyUI + AnimateDiff** | 节点式工作流，精细控制动画 |
| **ToonCrafter** | 两张关键帧之间自动生成中间帧 |
| **Stable Video Diffusion** | 图片转短视频，可做镜头过渡 |
| **LivePortrait** | 让角色插图动起来（说话/转头） |

### 后期 / 辅助

| 工具 | 用途 |
|------|------|
| **Real-ESRGAN** | 动漫图片超分辨率放大 |
| **Waifu2x** | 经典的二次元图片放大降噪 |
| **Upscayl** | 开源 AI 放大工具 |
| **Rerender** | 视频风格一致性修复 |
| **EbSynth** | 将 AI 生成帧同步到手绘视频 |

---

## 二、推荐工作流

### 入门路线 (零基础 → 能出图)

```
1. SeaArt / 哩布哩布        → 在线跑图（无需本地显卡）
2. 学会中文 Prompt 写法     → 哔哩哔哩搜索 "AI绘画prompt教程"
3. 下载 ComfyUI 本地部署     → 自由度更高，支持 ControlNet
4. 学习 LoRA 训练            → 练自己的角色/画风模型
5. 学习 AnimateDiff          → 静态图变动态
```

### 进阶路线 (从图到动画)

```
角色设计 → NovelAI / SD → 多视图生成
   ↓
场景/背景 → SD + ControlNet depth → 透视一致
   ↓
关键帧 → SD + LoRA → 保持角色一致性
   ↓
补帧 → ToonCrafter / RIFE → 帧间插值
   ↓
视频合成 → ComfyUI AnimateDiff → 输出成品
```

---

## 三、关键技术概念

| 概念 | 说明 |
|------|------|
| **LoRA** | 轻量微调模型，训练指定角色/画风（几十MB） |
| **ControlNet** | 控制生成结构：姿态、深度、边缘、线稿 |
| **IP-Adapter** | 图片风格迁移，参考图驱动生成 |
| **CLIP** | 理解文字描述的模型，决定画风 |
| **VAE** | 改善生成色彩和细节 |
| **Inpainting** | 局部重绘，修改画面特定区域 |
| **T2I / I2I** | 文生图 / 图生图 |
| **AnimateDiff Motion** | 动作模型，控制角色运动轨迹 |

---

## 四、学习资源

### B站教程（中文，零门槛）

| UP主 | 内容方向 |
|------|---------|
| **秋叶aaaki** | SD 整合包 + 教程，适合入门 |
| **Nenly同学** | SD 系统课程，讲解详细 |
| **Krenz** | 绘画基础 + AI 辅助创作 |
| **吴东林** | ComfyUI 工作流教学 |
| **白小二** | NovelAI / SD 实操教程 |

### 英文资源

| 资源 | 链接 |
|------|------|
| Stable Diffusion 官方文档 | stability.ai |
| Civitai（模型下载站） | civitai.com（需梯子） |
| ComfyUI 官方示例 | github.com/comfyanonymous/ComfyUI |
| Hugging Face 模型库 | huggingface.co |

---

## 五、国内模型/素材站

| 站点 | 说明 |
|------|------|
| **哩布哩布 LiblibAI** | liblibai.com — 最大中文 SD 模型站，在线跑图 |
| **SeaArt** | seaart.ai — 在线工具 + 模型社区 |
| **吐司 TusiArt** | tusiapp.com — 模型分享 |
| **元素法典** | SD 模型中文教程站 |
| **AI Space** | ai-space.com — 国内模型聚合 |

---

## 六、实用 Prompt 示例

### 二次元角色
```
masterpiece, best quality, 1girl, anime style, dynamic pose,
detailed eyes, school uniform, spring atmosphere, cherry blossoms,
natural lighting, depth of field
```

### 动画场景
```
anime background, cityscape at sunset, wide shot, cinematic lighting,
volumetric clouds, street lamps, atmospheric perspective,
ghibli inspired, vivid colors
```

### 动作帧
```
dynamic action shot, mid-jump, flowing hair, motion blur,
anime style, impact frames, speed lines, highly detailed,
sharp focus
```

---

## 七、硬件建议

| 配置 | 能做什么 |
|------|---------|
| 无独显 / 集显 | SeaArt / 哩布哩布 在线跑图 |
| RTX 3060 12GB | SD 本地部署 + LoRA 训练 |
| RTX 4090 24GB | SD + AnimateDiff + 视频生成 |
| Mac M 系列 | Draw Things / DiffusionBee 轻量使用 |
| 云 GPU | AutoDL / 恒源云 租用（按小时计费） |
