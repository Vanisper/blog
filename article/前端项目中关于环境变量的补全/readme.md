# 前端项目中关于环境变量的补全

如题，这应该是在 nodejs 项目中经常遇到的问题，最常见的一个场景是 `__filename` 和 `__dirname` 丢失的问题。

>
> 这里有一个讲的比较好的文章：<https://blog.csdn.net/weixin_43459866/article/details/125367138>
>
> 本文探讨了 CommonJS 和 ESM 模块系统中的 `__filename` 和 `__dirname` 变量。
>
> 在 CommonJS 中，`__filename` 和 `__dirname` 是内置变量，但在 ESM 中并未注入此变量。
>
> 在 ESM 中，通过 `import.meta.url` 获取模块的路径信息，也就是 `__filename`；再结合 `path` 模块来模拟 `__dirname` 的行为。
> ``` js
> import path from 'path';
> import { fileURLToPath } from 'url';
> 
> const __filename = fileURLToPath(import.meta.url);
> const __dirname = path.dirname(__filename);
> ```
>
> `import.meta` 提供模块的上下文信息，与 CommonJS 中的模块变量作用相似，但遵循不同的规范。
>

然而本文则想探讨的是有哪些方式可以实现环境变量的补全，或者应该说 **注入环境变量**。

### 1. 注入到 `globalThis` 关键字下

> 本方案来自于：<https://github.com/Coolchickenguy/Coolchickenguy.github.io/blob/main/lib/es_patches.js>

``` js
// es_patches.js
import path from "path";
import { fileURLToPath } from "url";

export function pathPatch(importMeta) {
  globalThis.__filename = fileURLToPath(importMeta.url);
  globalThis.__dirname = path.dirname(__filename);
}

// ... other patch ...

export default function (importMeta) {
  pathPatch(importMeta);
  // ... other patch ...
}
```

使用：

> 详见
> - 全局注入：https://github.com/Coolchickenguy/Coolchickenguy.github.io/blob/main/cleanup.js#L2-L4
> - 按需注入：https://github.com/Coolchickenguy/Coolchickenguy.github.io/blob/main/lib/build-node.js#L11-L12

``` js
import fix from "./es_patches.js";

// 按需注入，调用时需要将当前环境的 `import.meta` 手动传入
export default function(meta, ...args){
  fix(meta);
  console.log(__dirname)
  // ...
}
```

### 2. 编写编译构建工具的插件，实现注入（vite）

> 匹配代码中待注入的关键字，然后替换成相应的执行结果
>
> 本方案来自：https://github.com/4chao/preset/blob/master/build/vite-plugin-define.ts#L24-L45

``` ts
import path from 'node:path'
import process from 'node:process'
import type { Plugin } from 'vite'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type func<P extends any[] = any[], R = any> = (...args: P) => R
type DefineFunc = (code: string, id: string) => string | func

export default function () {
  const map = <Record<string, DefineFunc>>{
    [['__', 'filename'].join('')]: (_, id) => `"${path.relative(process.cwd(), id)}"`,
    [['__', 'dirname'].join('')]: (_, id) => `"${path.dirname(path.relative(process.cwd(), id))}"`,
  } // 允许拓展
  const keys = Object.keys(map).join('|') // `__filename|__dirname` 正则表达式的一部分

  return <Plugin>{
    name: 'vite-plugin-define',
    enforce: 'post',
    transform: (code: string, id: string) => {
      let arr: func[] = []
      code = code.replace(new RegExp(`(${keys})`, 'g'), (org, k) => {
        let r = map[k](code, id)
        if (typeof r === 'string') return r
        else arr.push(r)
        return org
      })
      arr.forEach(e => (code = e(code)))
      return code
    },
  }
}
```

做好类型标注：

``` ts
// declare let __filename: string; // 这种标注的优先级更高，但却是局部的标注
declare global {
  let __filename: string
  // ...
}
```
