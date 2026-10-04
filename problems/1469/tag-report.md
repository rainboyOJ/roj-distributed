最终 tag：字符串、哈希
理由：统计 A+B+A 形子串（|A|≥k）需枚举分界并用字符串哈希求 LCP 统计可取的 |A|，jev 的 Manacher 求的是回文（A+B+reverse(A)），不适用于本题。
与 jev：一致（jev 建议 字符串(0.89)、Manacher(0.58)、哈希(0.44)，置信度 0.96）
