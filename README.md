# runtime-shims

迁移到 acde 的网页应用共用的运行时兜底脚本。每个文件针对 libacde 的一个缺口，用特性检测，运行时修好后删掉对应文件即可。

| 文件 | 缺口 |
| --- | --- |
| `shims/performance-measure.js` | `performance.measure` 引用不存在的 mark 时抛错 |
| `shims/node-accessors.js` | `Node.prototype.nodeType`、`nodeName` 对文本节点等返回 0 或空串，DOMPurify 等通过原型取值的库会误删节点 |

## 用法

应用的构建脚本在整理出 `public/` 之后执行：

```bash
python3 "$root/../../packages/runtime-shims/install.py" "$public"
```

它把所有兜底合成 `public/acde-compat.js`，并给每个 HTML 的 `<head>` 加上 `<script src="/acde-compat.js">`，同时删掉 `<noscript>`（运行时会把它当可见内容渲染）。默认用根路径，适合声明 `"entry": "/"`、由后台托管 `public/` 的应用；页面作为应用包文件直接加载时，acdev 不接受根路径引用，第二个参数传 `./` 改用相对路径。

缺口细节见总仓 `.scratch/community/runtime-gaps.md`。
