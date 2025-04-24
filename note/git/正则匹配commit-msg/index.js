/**
 * 将 UCS-4 码点转换为 UTF-16 代理对
 * @param {number} codePoint - UCS-4 码点 (如 0x1F600)
 * @returns {string} UTF-16 字符串
 */
function ucs4ToUcs2(codePoint) {
    // 验证输入范围
    if (codePoint < 0x0 || codePoint > 0x10FFFF) {
      throw new Error(`Invalid code point: 0x${codePoint.toString(16)}`);
    }
  
    // 基本多文种平面 (BMP) 直接转换
    if (codePoint <= 0xFFFF) {
      return String.fromCodePoint(codePoint);
    }
  
    // 计算代理对
    const offset = codePoint - 0x10000;
    const highSurrogate = 0xD800 + (offset >> 10);
    const lowSurrogate = 0xDC00 + (offset & 0x3FF);
    return String.fromCharCode(highSurrogate, lowSurrogate);
}

/**
 * 
 * @param {string} emoji 
 * @returns 
 */
function aaa(emoji) {
    const length = emoji.length
    return Array.from({ length }).map((_, index) => {
        const res = emoji.charCodeAt(index).toString(16)
        return res
    })
}

const list = [
    ["00002600","00002B55"],
    ["0001F1E0","0001F1FF"],  // flags (iOS)
    ["0001F300","0001F5FF"],  // symbols & pictographs
    ["0001F600","0001F64F"],  // emoticons
    ["0001F680","0001F6FF"],  // transport & map symbols
    ["0001F700","0001F77F"],  // alchemical symbols
    ["0001F780","0001F7FF"],  // Geometric Shapes Extended
    ["0001F800","0001F8FF"],  // Supplemental Arrows-C
    ["0001F900","0001F9FF"],  // Supplemental Symbols and Pictographs
    ["0001FA00","0001FA6F"],  // Chess Symbols
    ["0001FA70","0001FAFF"],  // Symbols and Pictographs Extended-A
]

list.forEach((lines, index) => {
    console.log(index);
    lines.forEach((item, idx) => {
        console.log(item, aaa(ucs4ToUcs2(`0x${item}`)));
    })
})


