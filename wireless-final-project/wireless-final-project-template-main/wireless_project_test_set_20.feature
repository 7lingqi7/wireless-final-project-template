# language: zh-CN
功能: 无线通信期末项目测试集 20 条
  作为无线通信技术课程教师
  我希望使用公开测试集检查学生项目是否满足 PRD
  从而评价学生的设计、mock 测试、代码实现、分析和解释能力

  背景:
    假如 学生项目包含教师给定的 PRD.md
    并且 学生项目包含 DESIGN.md
    并且 学生项目包含 TEST_PLAN.md
    并且 学生项目包含 MOCK_TEST_REPORT.md
    并且 学生项目包含 AI_LOG.md
    并且 学生项目包含 main.py
    并且 学生项目包含 src/ 和 tests/ 目录
    并且 教师提供 UTF-8 编码的 Test.txt

  @testset @public @structure
  场景: TC-T-001 项目目录包含必需提交物
    当 教师检查学生项目根目录
    那么 应存在 DESIGN.md
    并且 应存在 TEST_PLAN.md
    并且 应存在 MOCK_TEST_REPORT.md
    并且 应存在 AI_LOG.md
    并且 应存在 main.py
    并且 应存在 src/ 目录
    并且 应存在 tests/ 目录

  @testset @public @design
  场景: TC-T-002 DESIGN.md 覆盖固定系统链路
    当 教师阅读 DESIGN.md
    那么 文档应说明 Source Encode
    并且 文档应说明 Encrypt 或 Scramble
    并且 文档应说明 Channel Encode
    并且 文档应说明 Frame Build
    并且 文档应说明 QPSK Modulate 和 QPSK Demodulate
    并且 文档应说明 Channel、Synchronization、Channel Decode 和 Source Decode

  @testset @public @mock
  场景: TC-T-003 MOCK_TEST_REPORT.md 包含设计修订记录
    当 教师阅读 MOCK_TEST_REPORT.md
    那么 报告应列出至少 3 个 mock 测试场景
    并且 报告应说明至少 1 个设计风险或缺陷
    并且 报告应说明 DESIGN.md 的修订内容

  @testset @public @source
  场景: TC-T-004 UTF-8 中文文本源编码可逆
    假如 Test.txt 内容为 无线通信技术课程要求学生理解调制编码信道和接收机处理
    当 系统执行源编码得到 bitstream
    并且 系统执行源解码
    那么 恢复文本应与 Test.txt 完全一致
    并且 bitstream 长度应为 8 的整数倍

  @testset @public @frame
  场景: TC-T-005 帧结构包含 PRD 要求字段
    假如 输入 payload 长度为 2400 bit
    当 系统执行 Frame Build
    那么 生成的帧应包含 preamble
    并且 生成的帧应包含 length 字段
    并且 生成的帧应包含 payload 字段
    并且 生成的帧应包含 checksum 或 CRC 字段

  @testset @public @frame
  场景: TC-T-006 帧封装和解析可逆
    假如 输入 payload 为固定随机 bitstream
    当 系统执行 Frame Build
    并且 系统执行 Frame Parse
    那么 解析得到的 payload 应与输入 payload 一致
    并且 解析得到的 length 应等于原始 payload bit 数

  @testset @public @scramble
  场景: TC-T-007 扰码或加密模块可逆
    假如 输入 bitstream 为非空随机比特序列
    并且 使用固定密钥或固定扰码种子 2026
    当 系统执行 Scramble 或 Encrypt
    并且 系统执行 Descramble 或 Decrypt
    那么 输出 bitstream 应与输入 bitstream 完全一致

  @testset @public @coding
  场景: TC-T-008 信道编码和译码在无噪声下可逆
    假如 输入 bitstream 为固定随机比特序列
    并且 信道为无噪声信道
    当 系统执行 Channel Encode
    并且 系统执行 Channel Decode
    那么 输出 bitstream 应与输入 bitstream 完全一致

  @testset @public @qpsk
  场景: TC-T-009 QPSK 映射符合 PRD
    假如 输入比特对依次为 00 01 11 10
    当 系统执行 QPSK Modulate
    那么 星座映射应为 Gray 编码
    并且 00 应映射到第一象限
    并且 01 应映射到第二象限
    并且 11 应映射到第三象限
    并且 10 应映射到第四象限

  @testset @public @qpsk
  场景: TC-T-010 QPSK 无噪声调制解调无误码
    假如 输入 bitstream 长度为偶数
    并且 信道为无噪声信道
    当 系统执行 QPSK Modulate
    并且 系统执行 QPSK Demodulate
    那么 解调 bitstream 应与输入 bitstream 完全一致

  @testset @public @padding
  场景: TC-T-011 QPSK padding 能被 length 字段去除
    假如 原始 payload bit 数为奇数
    当 系统执行帧封装和 QPSK 调制
    并且 接收端完成解调和解析
    那么 接收端应根据 length 字段去除 padding
    并且 恢复 payload 长度应等于原始 payload bit 数

  @testset @public @awgn
  场景: TC-T-012 AWGN 信道固定 seed 可复现
    假如 输入 QPSK 符号序列固定
    并且 SNR 为 12 dB
    并且 随机种子为 2026
    当 系统两次执行 AWGN 信道
    那么 两次输出符号序列应完全一致或在数值容差内一致

  @testset @public @sync
  场景: TC-T-013 同步模块检测 25 符号前置偏移
    假如 发送帧前添加 25 个随机噪声符号作为偏移
    并且 帧中包含已知 preamble
    并且 SNR 为 12 dB
    当 系统执行 Synchronization
    那么 系统应报告检测到的帧起点
    并且 检测误差应不超过 1 个符号

  @testset @public @metrics
  场景: TC-T-014 metrics.json 包含最低字段
    假如 Test.txt 为约 300 字中文课程描述
    并且 调制方式为 QPSK
    并且 信道为 AWGN
    并且 SNR 为 12 dB
    并且 随机种子为 2026
    当 运行 python main.py --input Test.txt --output results/received.txt --snr 12 --seed 2026 --mod qpsk --channel awgn
    那么 程序应正常退出
    并且 应生成 results/received.txt
    并且 应生成 results/metrics.json
    并且 metrics.json 应包含 snr_db、seed、modulation、channel、payload_bits 字段
    并且 metrics.json 应包含 ber、fer、text_match_rate、checksum_pass、sync_start_index 字段

  @testset @public @end_to_end
  场景: TC-T-015 SNR 12 dB 下端到端恢复完全一致
    假如 Test.txt 为约 300 字中文课程描述
    并且 调制方式为 QPSK
    并且 信道为 AWGN
    并且 SNR 为 12 dB
    并且 随机种子为 2026
    当 运行 python main.py --input Test.txt --output results/received.txt --snr 12 --seed 2026 --mod qpsk --channel awgn
    那么 程序应正常退出
    并且 应生成 results/received.txt
    并且 应生成 results/metrics.json
    并且 results/received.txt 应与 Test.txt 完全一致
    并且 metrics.json 中 text_match_rate 应等于 1.0

  @testset @public @plots
  场景: TC-T-016 生成至少两类可视化图表
    假如 Test.txt 为约 300 字中文课程描述
    并且 调制方式为 QPSK
    并且 信道为 AWGN
    并且 SNR 为 12 dB
    并且 随机种子为 2026
    当 运行 python main.py --input Test.txt --output results/received.txt --snr 12 --seed 2026 --mod qpsk --channel awgn
    那么 程序应正常退出
    并且 应生成 results/received.txt
    并且 应生成 results/metrics.json
    并且 results 目录应至少包含 constellation.png、ber_curve.png、sync_peak.png 中的两项

  @testset @public @cli
  场景: TC-T-017 统一命令行入口可运行
    假如 Test.txt 存在
    当 运行 python main.py --input Test.txt --output results/received.txt --snr 12 --seed 2026 --mod qpsk --channel awgn
    那么 程序应正常退出
    并且 不应要求人工交互输入

  @testset @public @ai_log
  场景: TC-T-018 AI_LOG.md 记录 AI 辅助过程
    当 教师阅读 AI_LOG.md
    那么 日志应包含至少 3 条关键 prompt 或交互摘要
    并且 日志应说明 AI 生成内容中哪些被人工修改
    并且 日志应说明最终采纳理由

  @testset @public @report
  场景: TC-T-019 实验分析报告解释关键结果
    当 教师阅读实验分析报告或 DESIGN.md 的结果分析部分
    那么 应解释 QPSK 星座图
    并且 应解释 BER 或 text_match_rate 随 SNR 的变化
    并且 应说明至少一个失败或误码原因

  @testset @public @anti_shortcut
  场景: TC-T-020 项目不得绕过无线链路直接复制文件
    当 教师检查源代码和运行日志
    那么 不应存在直接将 Test.txt 复制为 results/received.txt 的主流程
    并且 received.txt 应由接收端解码流程生成
