# 有无相生的道理 · 电影感重制版

90 秒 / 1920×1080 / 30 fps / 2700 帧，中文字幕叙事，无人声。画幅上下各有 74 像素遮幅，字幕位于下方遮幅。以杯子为贯穿意象，用三维器皿、房屋、三十辐车轮和程序山水说明形体、关系与空间。所有模型、纹理、环境光、画面和音乐由代码构建；没有使用图片、视频、音乐或语音生成模型，也没有使用素材视频。

本轮保留原有论述与时长，重点重做视觉：23 个镜头；青釉陶器、旧木与灰泥材质；代码构建的 HDR 反射环境；侧逆光和柔化阴影；真实深度纹理驱动的镜头虚化；室内窗光与羽化光束；车毂近景；七根实体琴弦；宣纸书法插镜。画面由明亮的模型陈列改成暗背景器物摄影与室内视角。

## 内容依据与解读范围

本片以通行本《道德经》第二章与第十一章为线索。第二章的“有无相生，难易相成，长短相较”用于说明相对概念相待而显；第十一章的车毂、器皿和房屋用于说明实体与可用空间的配合。二者没有被当成完全相同的论证，也不代表对“有无”的唯一哲学解释。

原文核对日期：2026-10-22。[中国哲学书电子化计划《道德经》](https://ctext.org/dao-de-jing/ens)，[第十一章平行文本](https://ctext.org/text.pl?if=en&node=11602&show=parallel)。本地网页全文读取受 403 限制，原文片段通过该文献库的搜索索引与平行文本检索交叉核对。影片不复用网站的现代译文。

63–75 秒的音乐间歇、画面留白、话语停顿，以及片尾“给事物以形，也给可能留白”，属于现代创作联想，画面已注明。器皿、房屋、车轮是讲解模型，不是考古复原。

## 制作与复现

Three.js 0.160.1 渲染实体模型。`film.js` 提供几何构建与内容，`cinema.js` 重设材质、环境、灯光、摄影机与后期；在 HalfFloat 渲染目标中保存 HDR 色彩和深度，再经景深与色调映射输出。陶器具有内外表面；水面使用折射材质。字体和字幕由 Canvas 叠加，全部动画由绝对帧时间计算。音轨沿用已合成的原创拨弦、气声与轻打击，按同一时间轴合成。

本项目使用 Python 3.12.7；固定依赖要求 Python 3.12 或以上，另需系统 PATH 中可用的 FFmpeg/FFprobe：

```text
python -m pip install -r requirements.txt
python -m playwright install chromium
python build.py --preview-only
python build.py
```

Windows 上有可用独显时，先执行 `python gpu_probe.py` 验证实际显卡、字体就绪及跨场景重复捕获，再执行 `python build.py --angle d3d11`。未通过验证时使用默认 SwiftShader。不同显卡或后端之间不承诺像素哈希相同；每个所选后端均应单独核验。示例在一次 Windows / D3D11 制作中通过八个采样点的跨场景重复捕获测试；这不代表其他设备已验证。

已有 `output/visual.mp4` 和 `output/score.wav` 时，可用 `python build.py --finish-only` 完成交付编码与核验。本项目在父目录 `.browsers` 存在时会使用其中的 Chromium；其他机器可使用 Playwright 的默认安装路径。若固定版本依赖在目标平台不可用，应选择兼容版本并重新完成画面与音轨核验。

文件：`film.js`、`cinema.js` 为场景；`plan.json` 为章节、镜头帧表与内容边界；`score.py` 为配乐；`qa.py` 检查跨场景重复捕获、字幕宽度和全部 22 个切点；`scripts/` 包含逐帧捕获和独立 MP4 检查工具。

## 许可与来源

- Three.js 0.160.1，MIT，`assets/THREE-LICENSE.txt`；[发布文件](https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.min.js)。
- Noto Sans CJK SC Regular，SIL OFL 1.1，`fonts/OFL-LICENSE.txt`；[Noto 项目](https://github.com/notofonts/noto-cjk)。
- 马善政 Ma Shan Zheng，SIL OFL 1.1，`fonts/MaShanZheng-OFL.txt`；[Google Fonts 字体目录](https://github.com/google/fonts/tree/main/ofl/mashanzheng)。
- 《道德经》古文为公版文献；本片的通俗解释与现代联想为本项目创作。


本目录独立运行；从这里执行命令。`gpu_probe.py` 仅用于 Windows D3D11，请先创建 `preview` 目录；其他平台使用默认 SwiftShader。预览图见仓库 `docs/`。影片与镜头内容是主题专用示例，不能仅修改标题就得到其他主题影片。
