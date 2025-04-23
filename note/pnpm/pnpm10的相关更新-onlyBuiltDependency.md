相关参考链接：
- https://socket.dev/blog/pnpm-10-0-0-blocks-lifecycle-scripts-by-default
- https://blog.csdn.net/u012024114/article/details/145514733
- https://github.com/pnpm/pnpm.io/pull/624

pnpm10 现在会阻止生命周期脚本，如果想要允许某些项目执行其生命周期脚本，需要配置 `onlyBuiltDependencies`。

如果一个依赖项存在生命周期脚本，但是没有在 `onlyBuiltDependencies` 中配置，那么在 pnpm10 安装依赖时会有警告，如果这是故意的行为，则可以在 `ignoredBuiltDependencies` 中配置之，以明确不执行这些依赖的生命周期脚本（例如 `core-js` 的 `postinstall` 指令只是一个捐赠的log，对依赖本身没有实际构建作用，所以可以明确忽略执行），这样就不会有控制台警告了。

> [!TIP]
>
> 生命周期脚本包括开发人员在其 package.json 文件的 scripts 部分中定义的 preinstall、install、postinstall、prepublish、prepare 等，这些脚本由软件包管理器自动执行。

上面的更新是为了防止一些依赖库执行一些恶意的脚本，例如 [Rspack 供应链攻击](https://socket.dev/blog/rspack-supply-chain-attack) 。
