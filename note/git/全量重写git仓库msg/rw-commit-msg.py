from typing import Optional, TypedDict
import re
from git_filter_repo import Commit

class CommitMsgResult(TypedDict):
    emoji: Optional[str]
    emoji_left: Optional[str]
    type: str
    scope: Optional[str]
    emoji_center: Optional[str]
    subject: str
    ticket: Optional[str]
    ticket_number: Optional[str]
    emoji_right: Optional[str]
    raw: re.Match[str]


# /(\ud83c[\udf00-\udfff])|(\ud83d[\udc00-\ude4f\ude80-\udeff])|[\u2600-\u2B55]/ // 这个是网上常见的回答，但是不完全
# /(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])/ // 这个是有很多冗余
# https://www.regextester.com/106421
# https://nekonull.me/share/build-emoji-regex/
# https://stackoverflow.com/a/26740753/26849265
# ---
# Python 正则表达式，js 中组合式 Unicode 的写法在 python 需要转换
# ---
# [\u2600-\u2B55]  => [\U00002600-\U00002B55] (基础符号)
# ---
# \ud83c[\udde0-\uddff] => [\U0001F1E0-\U0001F1FF]  # 国旗（iOS区域指示符组合）
# \ud83c[\udf00-\udfff] => [\U0001F300-\U0001F5FF] (颜色/图形符号)
# ---
# \ud83d[\ude00-\ude4f] => [\U0001F600-\U0001F64F] (表情符号)
# \ud83d[\ude80-\udeff] => [\U0001F680-\U0001F6FF] (交通工具/地图符号)
# \ud83d[\udf00-\udf7f] => [\U0001F700-\U0001F77F]  # 炼金术符号
# \ud83d[\udf80-\udfff] => [\U0001F780-\U0001F7FF]  # 几何图形扩展
# ---
# \ud83e[\udc00-\udcff] => [\U0001F800-\U0001F8FF]  # 补充箭头-C
# \ud83e[\udd00-\uddff] => [\U0001F900-\U0001F9FF] (补充物品/脸谱)
# \ud83e[\ude00-\ude6f] => [\U0001FA00-\U0001FA6F]  # 棋类符号（需与上一行范围重叠）
# \ud83e[\ude70-\udeff] => [\U0001FA70-\U0001FAFF] (运动/工具/扩展符号)
# ---
commit_msg_pattern = r"^((?P<emoji_left>(?::\w*:|[\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF]))\s*)?(?P<type>\w+)(?:\((?P<scope>[^)]*)\))?!?:\s*((?P<emoji_center>(?::\w*:|[\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF]))\s*)?(?P<subject>(?:(?!#).)*(?:(?!\s).))(?:\s(?P<ticket>#(?P<ticket_number1>\w+)|\(#(?P<ticket_number2>\w+)\)))?(?:\s(?P<emoji_right>(?::\w*:|[\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF])))?$"

def parse_commit_msg(commit_msg: str) -> Optional[CommitMsgResult]:
    match = re.match(commit_msg_pattern, commit_msg, re.M)
    if not match:
        return None

    ticket_number = match.group("ticket_number1") or match.group("ticket_number2")
    emoji = match.group("emoji_left") or match.group("emoji_center") or match.group("emoji_right")

    return {
        "emoji": emoji,
        "emoji_left": match.group("emoji_left"),
        "type": match.group("type"),
        "scope": match.group("scope"),
        "emoji_center": match.group("emoji_center"),
        "subject": match.group("subject"),
        "ticket": match.group("ticket"),
        "ticket_number": ticket_number,
        "emoji_right": match.group("emoji_right"),
        "raw": match
    }

# print(parse_commit_msg("✨ feat(unicode): ✨   adasas  sfsd :das: #1d1w ✨"))

# 新封装的函数：修改 msg 中 emoji 的位置
def move_emoji_to_left(commit_msg: str) -> str:
    parsed_result = parse_commit_msg(commit_msg)
    if not parsed_result:
        return commit_msg  # 返回原始的 msg 如果没有匹配成功
    emoji_left = parsed_result["emoji_left"]
    if emoji_left:
        return commit_msg

    emoji = parsed_result["emoji"]
    if not emoji:
        return commit_msg
    
    # 将剩下的 emoji 顺次移动第一个 emoji 的位置到左边
    emoji_center = parsed_result["emoji_center"]
    if emoji_center:
        # 将 emoji_center 移动到 emoji_left 的位置，并移除 emoji_center 原来的位置的 emoji
        commit_msg = commit_msg.replace(f" {emoji_center}", "", len(emoji_center) + 1).strip()
        commit_msg = f"{emoji} {commit_msg}".strip()
        return commit_msg
    
    emoji_right = parsed_result["emoji_right"]
    if emoji_right:
        # 将 emoji_right 移动到 emoji_left 的位置，并移除 emoji_right 原来的位置的 emoji
        commit_msg = commit_msg.replace(f" {emoji_right}", "", len(emoji_right) + 1).strip()
        commit_msg = f"{emoji} {commit_msg}".strip()
        return commit_msg

    return commit_msg

# def callback(commit: Commit, _):
#     msg = commit.message.decode("utf-8")
#     commit.message = move_emoji_to_left(msg).encode("utf-8")

if __name__ == 'builtins':
    commit: Commit
    msg = commit.message.decode("utf-8")
    commit.message = move_emoji_to_left(msg).encode("utf-8")
