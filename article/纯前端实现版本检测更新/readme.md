# 纯前端实现版本检测更新

基本原理就是定时器轮询请求前端构建产物中的某一个文件，这个文件通常是 `index.html`，这是比较通用地实现这一需求的一个办法（详见以下视频）。

> 视频来源：https://www.bilibili.com/video/BV1S14y1r74v

[![自动检测更新【渡一教育】](https://i1.hdslb.com/bfs/archive/b3b1fcdf9fe2a861b696ee89ba798dc766e906c1.jpg)](https://player.bilibili.com/player.html?isOutside=true&aid=788494845&bvid=BV1S14y1r74v&cid=1264741362&p=1)

这样的做法虽然说比较通用，但是分析整个 `index.html` 可能不是很好的做法，即使首页入口文件不复杂。如上面这个视频的一个评论说的：

> 我也遇到了这么个需求，因为是公司内部用的系统，所以不需要考虑流量，带宽问题。我的解决思路和老师的一样，定时请求。我是在vite中写了个自定义方法，每次打包时自动生成一个版本文件.json（就是个时间戳），然后在页面上定时请求这个json文件对比内容，不一致时提示用户刷新。

---

所以这里的关键是前端打包时需要产出一个与版本定义相关的文件，专门定义当前网站版本，直接请求该文件，能减轻客户端分析版本变化的负担。并且这是前端可控的行为，所以这个方案可能更好。

> 以下方案来源于：https://seepine.com/vue/version
>
> 感谢原作者提供的方案！

这里借助 vite 的能力实现上述的需求。

### 1. vite 配置开启 manifest

``` js
// vite.config.*
export default {
  // ...
  // 增加此配置，开启manifest
  build: { manifest: true },
}
```

### 2. 构建项目

执行 `pnpm build` 命令后可以在 dist 目录中发现多出了文件 `dist/.vite/manifest.json`，记录着项目文件映射，之后我们可以利用此文件来判断前端项目是否更新了。

当然也可以通过其他方式比如后端增加一个版本接口，手动控制是否需要更新等等。

### 3. 编写更新文件

例如创建 src/hooks/version.ts 文件，并填入以下内容，其中注释部分可依据自己情况修改。

``` ts
import dayjs from 'dayjs'
import { NButton } from 'naive-ui'

let timer: number | undefined
/**
 * 版本更新监听器，当有新版本，右上角弹出消息通知
 * @param time 检查间隔，单位秒，默认5分钟
 */
export const useVersionUpdateListener = (time = 5 * 60) => {
  if (timer !== undefined) {
    return
  }
  if (import.meta.env.PROD) {
    let indexJs: string
    timer = setInterval(() => {
      window.axios
        .request({
          baseURL: '',
          // 此处就是访问第一步自动生成的映射文件，若是自己写后端接口，需更改此处
          url: `/.vite/manifest.json?t=${dayjs().valueOf()}`,
        })
        .then(res => {
          let file
          try {
            file = res['index.html'].file
          } catch (_) {
            return
          }
          if (!indexJs) {
            indexJs = file
          }
          if (indexJs !== file) {
            clearInterval(timer)
            // 此处使用了 `naive-ui` 全局通知弹窗，可自行改为你自己项目中的UI组件
            window.$notification.create({
              content: '发现新版本，点击获取最新版本。',
              meta: ' ',
              action: () =>
                h(
                  NButton,
                  {
                    size: 'small',
                    text: true,
                    type: 'primary',
                    onClick: () => {
                      window.location.reload()
                    },
                  },
                  { default: () => h('span', '刷新') },
                ),
            })
          }
        })
        .catch(() => {})
    }, time * 1000)
  }
}
```

### 4. 引用

在 App.vue 中引用即可

``` ts
onMounted(() => {
  useVersionUpdateListener()
  // useVersionUpdateListener(15*60) // 或控制每15分钟检测一次更新
})
```
