# 正则匹配 commit-msg

> 这里有一个示例：[demo.js](./demo.js)

## 1. 宽松模式 -- 适合用在脚本内的校验正则

https://regex101.com/r/rfUptQ/1

拆分：

```regex
/^
((?<emoji_left>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s*)?

(?<type>\w+)(?:\((?<scope>[^)]*)\))?!?:\s*

((?<emoji_center>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s*)?

(?<subject>(?:(?!#).)*(?:(?!\s).))

(?:\s
  (?<ticket>#(?<ticket_number>\w+)|\(#(?<ticket_number>\w+)\))
)?

(?:\s
  (?<emoji_right>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))
)?

$
/gm
```

完整：

```regex
/^((?<emoji_left>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s*)?(?<type>\w+)(?:\((?<scope>[^)]*)\))?!?:\s*((?<emoji_center>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s*)?(?<subject>(?:(?!#).)*(?:(?!\s).))(?:\s(?<ticket>#(?<ticket_number>\w+)|\(#(?<ticket_number>\w+)\)))?(?:\s(?<emoji_right>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55])))?$/gm
```

## 2. 严格模式 -- 适合给 commitlint 程序

https://regex101.com/r/czE2F8/1

拆分：

```regex
/^
((?<emoji_left>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s)?

(?<type>\w+)(?:\((?<scope>[^)]*)\))?!?:\s

((?<emoji_center>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s)?

(?<subject>(?:(?!#).)*(?:(?!\s).))

(?:\s
  (?<ticket>#(?<ticket_number>\w+)|\(#(?<ticket_number>\w+)\))
)?

(?:\s
  (?<emoji_right>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))
)?

$
/gm
```

完整：

```regex
/^((?<emoji_left>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s)?(?<type>\w+)(?:\((?<scope>[^)]*)\))?!?:\s((?<emoji_center>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s)?(?<subject>(?:(?!#).)*(?:(?!\s).))(?:\s(?<ticket>#(?<ticket_number>\w+)|\(#(?<ticket_number>\w+)\)))?(?:\s(?<emoji_right>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55])))?$/gm
```
