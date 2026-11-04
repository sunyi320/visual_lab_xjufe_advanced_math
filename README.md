<<<<<<< HEAD
# visual_lab_xjufe_advanced_math
=======
# 高等数学与线性代数可视化素材库

检索日期：2026-10-31（Asia/Shanghai）

## 快速索引

| 知识点 | 素材 | 类型 | 入口 |
|---|---|---|---|
| 导数、切线、极限、积分 | 3Blue1Brown Essence of Calculus | 动画 / Manim 源码 | `downloads/3b1b/chapter2_derivative.py`、`chapter8_integral.py`；[课程主页](https://www.3blue1brown.com/topics/calculus) |
| 线性变换、特征向量 | 3Blue1Brown Essence of Linear Algebra | 动画 / Manim 源码 | `downloads/3b1b/chapter3_linear_transform.py`、`chapter10_eigenvectors.py`；[课程主页](https://www.3blue1brown.com/topics/linear-algebra) |
| 平面几何变换 | 鸢尾花书 Book 4 Chapter 08 | Python / Plotly / Streamlit / Jupyter | `downloads/iris_book4/`；[仓库](https://github.com/Visualize-ML/Book4_Power-of-Matrix) |
| SVD 几何意义与性质 | 鸢尾花书 Book 4 Chapter 15 | Python / NumPy / Matplotlib / Jupyter | `downloads/iris_book4/Bk4_Ch15_01.ipynb`、`Bk4_Ch15_02.ipynb` |
| 多元微积分、梯度、曲面、积分 | Math Insight | 交互网页 / applet | [mathinsight.org](https://mathinsight.org/) |
| 微积分与微分方程 | Mathlets | 交互网页 | [mathlets.org/mathlets](https://mathlets.org/mathlets/) |
| 线性代数 | Immersive Linear Algebra | 交互教材 / 动画 | [immersivemath.com/ila](https://immersivemath.com/ila/index.html) |
| 线性代数 | Interactive Linear Algebra（Georgia Tech） | 在线教材 / 交互演示 | [textbooks.math.gatech.edu/ila](https://textbooks.math.gatech.edu/ila/) |
| 向量场、流线、散度直观 | Paul Falstad Vector Field | 交互模拟 | [falstad.com/vector](https://www.falstad.com/vector/) |
| 函数动画、滑块、流线 | Matplotlib 官方示例 | Python / Matplotlib | `downloads/matplotlib/`；[动画示例](https://matplotlib.org/stable/gallery/animation/index.html) |
| 微积分章节 Python | 鸢尾花书 Book 3 | Python / Jupyter | `sources/book3_ch15_listing.html`、`sources/book3_ch18_listing.html`；[仓库](https://github.com/Visualize-ML/Book3_Elements-of-Mathematics) |

## 说明

- `downloads/` 是本次检索中成功下载的公开源码或笔记本；每批下载结果和 SHA-256 记录在 `sources/download_batch*_results.json`。
- `sources/*_listing.html` 是 GitHub 目录页本地快照，可在联网时继续挑选同章节文件。
- 3Blue1Brown 的源码是 Manim 项目代码，通常需要按其仓库版本安装 Manim 才能复现；它适合作为“动画脚本”和课堂讲解参考。
- Mathlets 及部分旧 applet 可能依赖浏览器兼容层；使用前应在目标电脑上实际打开测试。
- 下载内容保留原作者版权和许可证信息；课堂使用、改编和再发布应遵守各仓库的 LICENSE。

## 本地素材运行建议

```text
Jupyter：打开 downloads/iris_book4/*.ipynb
Streamlit：streamlit run downloads/iris_book4/Streamlit_Bk4_Ch08_02.py
Manim：manim -pql downloads/3b1b/chapter2_derivative.py <SceneName>
Matplotlib：python downloads/matplotlib/simple_anim.py
```

## 检索记录

检索范围包含英文和中文关键词：calculus visualization、linear algebra visualization、interactive applet、Manim、Python animation、可视化、动态实现、梯度、积分、特征值、SVD、向量场等。结果优先保留官方教材、作者仓库和官方文档，并在本地目录中区分“已下载源码”和“在线入口”。

## 特别鸣谢

特别感谢Github上的开源资源，为本项目的顺利实施提供宝贵的资源，在此一并感谢。

>>>>>>> 29436d3 (Initial commit: upload visual_lab source code)
