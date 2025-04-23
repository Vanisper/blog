const pattern0 = /^((?<emoji_left>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s*)?(?<type>\w+)(?:\((?<scope>[^)]*)\))?!?:\s*((?<emoji_center>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s*)?(?<subject>(?:(?!#).)*(?:(?!\s).))(?:\s(?<ticket>#(?<ticket_number>\w+)|\(#(?<ticket_number>\w+)\)))?(?:\s(?<emoji_right>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55])))?$/
const pattern1 = /^((?<emoji_left>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s)?(?<type>\w+)(?:\((?<scope>[^)]*)\))?!?:\s((?<emoji_center>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55]))\s)?(?<subject>(?:(?!#).)*(?:(?!\s).))(?:\s(?<ticket>#(?<ticket_number>\w+)|\(#(?<ticket_number>\w+)\)))?(?:\s(?<emoji_right>(?::\w*:|\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f\ude80-\udeff]|[\u2600-\u2B55])))?$/

const demo = '🚀   feat(sc): :aa:   demo (#1qg12) :aa:'

console.log(demo.match(pattern0));
console.log(demo.match(pattern1));
