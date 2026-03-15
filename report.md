# BTSnoop HCI 日志解析报告

> 分层: HCI 命令/事件/ACL → L2CAP 信令/ATT

## 📊 概览统计

- **文件**: `examples/sample_hci.log`
- **总数据包**: 532
- **绝对时间**: 2026-01-14-00-00-03.967873 ~ 2026-01-14-00-02-56.550667
- **持续时间**: 172582.80 ms
- **HCI 命令**: 65 | **HCI 事件**: 221
- **ACL TX**: 246 | **ACL RX**: 0
- **错误数**: 0
- **连接句柄**: 0x0001

## ✅ Command Complete 验证

| 序号 | 相对(ms) | 绝对时间 | 命令 | OGF | OCF | 状态 |
|------|----------|----------|------|-----|-----|------|
| 2 | 95.23 | 2026-01-14-00-00-04.063095 | Reset | 0x03 | 0x003 | Success |
| 4 | 102.16 | 2026-01-14-00-00-04.070030 | Read Buffer Size | 0x04 | 0x005 | Success |
| 6 | 109.28 | 2026-01-14-00-00-04.077141 | Host Buffer Size | 0x03 | 0x033 | Success |
| 8 | 113.72 | 2026-01-14-00-00-04.081581 | Read Local Supported Features | 0x04 | 0x003 | Success |
| 10 | 118.15 | 2026-01-14-00-00-04.086014 | Write LE Host Supported | 0x03 | 0x06D | Success |
| 12 | 126.75 | 2026-01-14-00-00-04.094627 | LE Read Buffer Size | 0x08 | 0x002 | Success |
| 14 | 130.60 | 2026-01-14-00-00-04.098473 | Read Local Extended Features | 0x04 | 0x004 | Success |
| 16 | 136.36 | 2026-01-14-00-00-04.104225 | Write Page Timeout | 0x03 | 0x018 | Success |
| 18 | 140.34 | 2026-01-14-00-00-04.108208 | Read Page Timeout | 0x03 | 0x017 | Success |
| 20 | 144.02 | 2026-01-14-00-00-04.111885 | Set Event Mask | 0x03 | 0x001 | Success |

... 共 55 个

## 🔗 连接建立事件

| 序号 | 相对(ms) | 绝对时间 | 句柄 | 设备地址 | 状态 |
|------|----------|----------|------|----------|------|
| 89 | 73023.75 | 2026-01-14-00-01-16.991615 | 0x0001 | A8:6E:4E:43:F3:B9 | Success |
| 260 | 96068.70 | 2026-01-14-00-01-40.036560 | 0x0001 | A8:6E:4E:43:F3:B9 | Success |

## 🔴 断开连接事件

| 序号 | 相对(ms) | 绝对时间 | 句柄 | 原因 |
|------|----------|----------|------|------|
| 255 | 85749.03 | 2026-01-14-00-01-29.716896 | 0x0001 | Remote User Terminated Connection |

## 📋 详细通信流程

```
#     绝对时间(年-月-日-时-分-秒)            Delta(ms)    Direction          Type         OGF    OCF    Details
-----------------------------------------------------------------------------------------------------------------------------
1     2026-01-14-00-00-03.967873   0.00         Host->Controller   CMD          0x03   0x003  0x0C03 Reset
2     2026-01-14-00-00-04.063095   95.23        Controller->Host   EVENT        0x03   0x003  0x0E Command Complete -> Reset [Success]
3     2026-01-14-00-00-04.063377   95.51        Host->Controller   CMD          0x04   0x005  0x1005 Read Buffer Size
4     2026-01-14-00-00-04.070030   102.16       Controller->Host   EVENT        0x04   0x005  0x0E Command Complete -> Read Buffer Size [Success]
5     2026-01-14-00-00-04.070328   102.46       Host->Controller   CMD          0x03   0x033  0x0C33 Host Buffer Size
6     2026-01-14-00-00-04.077141   109.28       Controller->Host   EVENT        0x03   0x033  0x0E Command Complete -> Host Buffer Size [Success]
7     2026-01-14-00-00-04.077431   109.56       Host->Controller   CMD          0x04   0x003  0x1003 Read Local Supported Features
8     2026-01-14-00-00-04.081581   113.72       Controller->Host   EVENT        0x04   0x003  0x0E Command Complete -> Read Local Supported Features [Success]
9     2026-01-14-00-00-04.081833   113.96       Host->Controller   CMD          0x03   0x06D  0x0C6D Write LE Host Supported
10    2026-01-14-00-00-04.086014   118.15       Controller->Host   EVENT        0x03   0x06D  0x0E Command Complete -> Write LE Host Supported [Success]
11    2026-01-14-00-00-04.086273   118.40       Host->Controller   CMD          0x08   0x002  0x2002 LE Read Buffer Size
12    2026-01-14-00-00-04.094627   126.75       Controller->Host   EVENT        0x08   0x002  0x0E Command Complete -> LE Read Buffer Size [Success]
13    2026-01-14-00-00-04.095001   127.14       Host->Controller   CMD          0x04   0x004  0x1004 Read Local Extended Features
14    2026-01-14-00-00-04.098473   130.60       Controller->Host   EVENT        0x04   0x004  0x0E Command Complete -> Read Local Extended Features [Success]
15    2026-01-14-00-00-04.099190   131.32       Host->Controller   CMD          0x03   0x018  0x0C18 Write Page Timeout
16    2026-01-14-00-00-04.104225   136.36       Controller->Host   EVENT        0x03   0x018  0x0E Command Complete -> Write Page Timeout [Success]
17    2026-01-14-00-00-04.104591   136.73       Host->Controller   CMD          0x03   0x017  0x0C17 Read Page Timeout
18    2026-01-14-00-00-04.108208   140.34       Controller->Host   EVENT        0x03   0x017  0x0E Command Complete -> Read Page Timeout [Success]
19    2026-01-14-00-00-04.108498   140.62       Host->Controller   CMD          0x03   0x001  0x0C01 Set Event Mask
20    2026-01-14-00-00-04.111885   144.02       Controller->Host   EVENT        0x03   0x001  0x0E Command Complete -> Set Event Mask [Success]
21    2026-01-14-00-00-04.112297   144.43       Host->Controller   CMD          0x04   0x001  0x1001 Read Local Version Information
22    2026-01-14-00-00-04.119026   151.16       Controller->Host   EVENT        0x04   0x001  0x0E Command Complete -> Read Local Version Information [Success]
23    2026-01-14-00-00-04.119209   151.34       Host->Controller   CMD          0x04   0x009  0x1009 Read BD_ADDR
24    2026-01-14-00-00-04.123306   155.44       Controller->Host   EVENT        0x04   0x009  0x0E Command Complete -> Read BD_ADDR [Success]
25    2026-01-14-00-00-04.123558   155.69       Host->Controller   CMD          0x03   0x044  0x0C44 Read Inquiry Mode
26    2026-01-14-00-00-04.129547   161.68       Controller->Host   EVENT        0x03   0x044  0x0E Command Complete -> Read Inquiry Mode [Success]
27    2026-01-14-00-00-04.129906   162.03       Host->Controller   CMD          0x03   0x05A  0x0C5A Read Default Erroneous Data Reporting
28    2026-01-14-00-00-04.134354   166.48       Controller->Host   EVENT        0x03   0x05A  0x0E Command Complete -> Read Default Erroneous Data Reporting [Success]
29    2026-01-14-00-00-04.134567   166.70       Host->Controller   CMD          0x03   0x058  0x0C58 Read Inquiry Response Transmit Power Level
30    2026-01-14-00-00-04.140572   172.70       Controller->Host   EVENT        0x03   0x058  0x0E Command Complete -> Read Inquiry Response Transmit Power Level [Success]
31    2026-01-14-00-00-04.140800   172.93       Host->Controller   CMD          0x03   0x056  0x0C56 Write Simple Pairing Mode
32    2026-01-14-00-00-04.150826   182.96       Controller->Host   EVENT        0x03   0x056  0x0E Command Complete -> Write Simple Pairing Mode [Success]
33    2026-01-14-00-00-04.151115   183.24       Host->Controller   CMD          0x08   0x001  0x2001 LE Set Event Mask
34    2026-01-14-00-00-04.158867   190.99       Controller->Host   EVENT        0x08   0x001  0x0E Command Complete -> LE Set Event Mask [Success]
35    2026-01-14-00-00-04.159073   191.21       Host->Controller   CMD          0x08   0x003  0x2003 LE Read Local Supported Features Page 0
36    2026-01-14-00-00-04.163734   195.87       Controller->Host   EVENT        0x08   0x003  0x0E Command Complete -> LE Read Local Supported Features Page 0 [Success]
37    2026-01-14-00-00-04.163979   196.10       Host->Controller   CMD          0x08   0x007  0x2007 LE Read Advertising Channel TX Power
38    2026-01-14-00-00-04.170288   202.42       Controller->Host   EVENT        0x08   0x007  0x0E Command Complete -> LE Read Advertising Channel TX Power [Success]
39    2026-01-14-00-00-04.170563   202.70       Host->Controller   CMD          0x08   0x01C  0x201C LE Read Supported States
40    2026-01-14-00-00-04.174614   206.75       Controller->Host   EVENT        0x08   0x01C  0x0E Command Complete -> LE Read Supported States [Success]
41    2026-01-14-00-00-04.174919   207.05       Host->Controller   CMD          0x08   0x00F  0x200F LE Read Filter Accept List Size
42    2026-01-14-00-00-04.180031   212.16       Controller->Host   EVENT        0x08   0x00F  0x0E Command Complete -> LE Read Filter Accept List Size [Success]
43    2026-01-14-00-00-04.234253   266.39       Host->Controller   CMD          0x02   0x00F  0x080F Write Default Link Policy Settings
44    2026-01-14-00-00-04.239288   271.42       Controller->Host   EVENT        0x02   0x00F  0x0E Command Complete -> Write Default Link Policy Settings [Success]
45    2026-01-14-00-00-04.239525   271.66       Host->Controller   CMD          0x03   0x045  0x0C45 Write Inquiry Mode
46    2026-01-14-00-00-04.244064   276.20       Controller->Host   EVENT        0x03   0x045  0x0E Command Complete -> Write Inquiry Mode [Success]
47    2026-01-14-00-00-04.244377   276.51       Host->Controller   CMD          0x03   0x01C  0x0C1C Write Page Scan Activity
48    2026-01-14-00-00-04.247917   280.06       Controller->Host   EVENT        0x03   0x01C  0x0E Command Complete -> Write Page Scan Activity [Success]
49    2026-01-14-00-00-04.248184   280.32       Host->Controller   CMD          0x03   0x01E  0x0C1E Write Inqury Scan Activity
50    2026-01-14-00-00-04.256180   288.31       Controller->Host   EVENT        0x03   0x01E  0x0E Command Complete -> Write Inqury Scan Activity [Success]
51    2026-01-14-00-00-04.256676   288.81       Host->Controller   CMD          0x03   0x01A  0x0C1A Write Scan Enable
52    2026-01-14-00-00-04.265266   297.40       Controller->Host   EVENT        0x03   0x01A  0x0E Command Complete -> Write Scan Enable [Success]
53    2026-01-14-00-00-04.265717   297.86       Host->Controller   CMD          0x03   0x024  0x0C24 Write Class of Device
54    2026-01-14-00-00-04.277023   309.16       Controller->Host   EVENT        0x03   0x024  0x0E Command Complete -> Write Class of Device [Success]
55    2026-01-14-00-00-04.277283   309.41       Host->Controller   CMD          0x08   0x008  0x2008 LE Set Advertising Data
56    2026-01-14-00-00-04.284073   316.21       Controller->Host   EVENT        0x08   0x008  0x0E Command Complete -> LE Set Advertising Data [Success]
57    2026-01-14-00-00-04.284325   316.46       Host->Controller   CMD          0x03   0x013  0x0C13 Write Local Name
58    2026-01-14-00-00-04.287888   320.02       Controller->Host   EVENT        0x03   0x013  0x0E Command Complete -> Write Local Name [Success]
59    2026-01-14-00-00-04.287979   320.11       Host->Controller   CMD          0x3F   0x01D  0xFC1D Vendor Command 0x01D
60    2026-01-14-00-00-04.293884   326.02       Controller->Host   EVENT        0x3F   0x01D  0x0E Command Complete -> Vendor Command 0x01D [Success]
61    2026-01-14-00-00-04.294159   326.30       Host->Controller   CMD          0x03   0x052  0x0C52 Write Extended Inqury Response
62    2026-01-14-00-00-04.325409   357.54       Controller->Host   EVENT        0x03   0x052  0x0E Command Complete -> Write Extended Inqury Response [Success]
63    2026-01-14-00-00-04.325623   357.75       Host->Controller   CMD          0x3F   0x007  0xFC07 Vendor Command 0x007
64    2026-01-14-00-00-04.327126   359.26       Controller->Host   EVENT        0x3F   0x007  0x0E Command Complete -> Vendor Command 0x007 [Success]
65    2026-01-14-00-00-04.327255   359.39       Host->Controller   CMD          0x3F   0x028  0xFC28 Vendor Command 0x028
66    2026-01-14-00-00-04.329803   361.93       Controller->Host   EVENT        0x3F   0x028  0x0E Command Complete -> Vendor Command 0x028 [Success]
67    2026-01-14-00-00-04.330002   362.13       Host->Controller   CMD          0x3F   0x029  0xFC29 Vendor Command 0x029
68    2026-01-14-00-00-04.348846   380.98       Controller->Host   EVENT        0x3F   0x029  0x0E Command Complete -> Vendor Command 0x029 [Success]
69    2026-01-14-00-00-04.349030   381.16       Host->Controller   CMD          0x3F   0x073  0xFC73 Vendor Command 0x073
70    2026-01-14-00-00-04.354958   387.09       Controller->Host   EVENT        0x3F   0x073  0x0E Command Complete -> Vendor Command 0x073 [Success]
71    2026-01-14-00-00-04.355225   387.36       Host->Controller   CMD          0x03   0x07D  0x0C7D Read Local OOB Extended Data
72    2026-01-14-00-00-04.361389   393.52       Controller->Host   EVENT        0x03   0x07D  0x0E Command Complete -> Read Local OOB Extended Data [Success]
73    2026-01-14-00-00-04.361847   393.98       Host->Controller   CMD          0x03   0x07A  0x0C7A Write Secure Connections Host Support
74    2026-01-14-00-00-04.367378   399.51       Controller->Host   EVENT        0x03   0x07A  0x0E Command Complete -> Write Secure Connections Host Support [Success]
75    2026-01-14-00-00-09.193336   5225.47      Host->Controller   CMD          0x03   0x01A  0x0C1A Write Scan Enable
76    2026-01-14-00-00-09.225281   5257.41      Controller->Host   EVENT        0x03   0x01A  0x0E Command Complete -> Write Scan Enable [Success]
77    2026-01-14-00-01-14.206909   70239.04     Host->Controller   CMD          0x03   0x01A  0x0C1A Write Scan Enable
78    2026-01-14-00-01-14.238197   70270.33     Controller->Host   EVENT        0x03   0x01A  0x0E Command Complete -> Write Scan Enable [Success]
79    2026-01-14-00-01-14.238647   70270.78     Host->Controller   CMD          0x08   0x006  0x2006 LE Set Advertising Parameters
80    2026-01-14-00-01-14.240051   70272.18     Controller->Host   EVENT        0x08   0x006  0x0E Command Complete -> LE Set Advertising Parameters [Success]
81    2026-01-14-00-01-14.240250   70272.38     Host->Controller   CMD          0x08   0x008  0x2008 LE Set Advertising Data
82    2026-01-14-00-01-14.241753   70273.89     Controller->Host   EVENT        0x08   0x008  0x0E Command Complete -> LE Set Advertising Data [Success]
83    2026-01-14-00-01-14.243378   70275.51     Host->Controller   CMD          0x08   0x00A  0x200A LE Set Advertising Enable
84    2026-01-14-00-01-14.246567   70278.70     Controller->Host   EVENT        0x08   0x00A  0x0E Command Complete -> LE Set Advertising Enable [Success]
85    2026-01-14-00-01-16.960777   72992.90     Controller->Host   EVENT        -      -      0x04 Connection Request
86    2026-01-14-00-01-16.963264   72995.39     Host->Controller   CMD          0x01   0x009  0x0409 Accept Connection Request
87    2026-01-14-00-01-16.964607   72996.74     Controller->Host   EVENT        -      -      0x0F Command Status
88    2026-01-14-00-01-16.991249   73023.38     Controller->Host   EVENT        -      -      0x20 Page Scan Repetition Mode Change
89    2026-01-14-00-01-16.991615   73023.75     Controller->Host   EVENT        -      -      0x03 Connection Complete Handle=0x0001 Addr=A8:6E:4E:43:F3:B9
90    2026-01-14-00-01-16.994949   73027.08     Host->Controller   CMD          0x01   0x00F  0x040F Change Connection Packet Type
91    2026-01-14-00-01-16.995102   73027.24     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
92    2026-01-14-00-01-16.996574   73028.70     Controller->Host   EVENT        -      -      0x0F Command Status
93    2026-01-14-00-01-16.996719   73028.85     Host->Controller   CMD          0x02   0x009  0x0809 OGF=0x02, OCF=0x009
94    2026-01-14-00-01-16.998016   73030.14     Controller->Host   EVENT        0x02   0x009  0x0E Command Complete -> OGF=0x02, OCF=0x009 [Success]
95    2026-01-14-00-01-16.998177   73030.31     Host->Controller   CMD          0x02   0x00D  0x080D Exit Sniff Mode
96    2026-01-14-00-01-16.999565   73031.70     Controller->Host   EVENT        0x02   0x00D  0x0E Command Complete -> Exit Sniff Mode [Success]
97    2026-01-14-00-01-17.000015   73032.15     Host->Controller   CMD          0x01   0x01B  0x041B OGF=0x01, OCF=0x01B
98    2026-01-14-00-01-17.001488   73033.62     Controller->Host   EVENT        -      -      0x0F Command Status
99    2026-01-14-00-01-17.001617   73033.75     Host->Controller   CMD          0x01   0x019  0x0419 Remote Name Request
100   2026-01-14-00-01-17.003014   73035.15     Controller->Host   EVENT        -      -      0x0F Command Status
101   2026-01-14-00-01-17.008240   73040.37     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
102   2026-01-14-00-01-17.008492   73040.62     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
103   2026-01-14-00-01-17.009689   73041.82     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
104   2026-01-14-00-01-17.009811   73041.94     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
105   2026-01-14-00-01-17.011024   73043.15     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
106   2026-01-14-00-01-17.011131   73043.26     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
107   2026-01-14-00-01-17.013634   73045.76     Controller->Host   EVENT        -      -      0x1B Event_0x1B
108   2026-01-14-00-01-17.019638   73051.77     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
109   2026-01-14-00-01-17.037056   73069.19     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
110   2026-01-14-00-01-17.037453   73069.59     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
111   2026-01-14-00-01-17.039795   73071.92     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
112   2026-01-14-00-01-17.040962   73073.09     Controller->Host   EVENT        -      -      0x07 Event_0x07
113   2026-01-14-00-01-17.041618   73073.75     Controller->Host   EVENT        -      -      0x1D Event_0x1D
114   2026-01-14-00-01-17.043076   73075.20     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
115   2026-01-14-00-01-17.043182   73075.31     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
116   2026-01-14-00-01-17.043282   73075.41     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
117   2026-01-14-00-01-17.045547   73077.68     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
118   2026-01-14-00-01-17.047043   73079.17     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
119   2026-01-14-00-01-17.048157   73080.29     Controller->Host   EVENT        -      -      0x0B Event_0x0B
120   2026-01-14-00-01-17.048492   73080.63     Controller->Host   EVENT        -      -      0x38 Event_0x38
121   2026-01-14-00-01-17.048607   73080.74     Host->Controller   CMD          0x01   0x01C  0x041C OGF=0x01, OCF=0x01C
122   2026-01-14-00-01-17.050095   73082.23     Controller->Host   EVENT        -      -      0x0F Command Status
123   2026-01-14-00-01-17.050186   73082.32     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
124   2026-01-14-00-01-17.051308   73083.43     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
125   2026-01-14-00-01-17.052582   73084.71     Controller->Host   EVENT        -      -      0x23 Event_0x23
126   2026-01-14-00-01-17.053963   73086.09     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
127   2026-01-14-00-01-17.055237   73087.37     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
128   2026-01-14-00-01-17.056816   73088.95     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
129   2026-01-14-00-01-17.071793   73103.93     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
130   2026-01-14-00-01-17.073906   73106.04     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
131   2026-01-14-00-01-17.074158   73106.30     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
132   2026-01-14-00-01-17.074203   73106.34     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
133   2026-01-14-00-01-17.076668   73108.80     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
134   2026-01-14-00-01-17.078171   73110.30     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
135   2026-01-14-00-01-17.083153   73115.28     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
136   2026-01-14-00-01-17.083687   73115.82     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004F,Dynamic_CID_0x004F)
137   2026-01-14-00-01-17.088371   73120.50     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
138   2026-01-14-00-01-17.090721   73122.85     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
139   2026-01-14-00-01-17.092316   73124.44     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
140   2026-01-14-00-01-17.120872   73153.00     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
141   2026-01-14-00-01-17.125938   73158.06     Controller->Host   EVENT        -      -      0x17 Event_0x17
142   2026-01-14-00-01-17.126297   73158.43     Host->Controller   CMD          0x01   0x00C  0x040C OGF=0x01, OCF=0x00C
143   2026-01-14-00-01-17.127655   73159.79     Controller->Host   EVENT        0x01   0x00C  0x0E Command Complete -> OGF=0x01, OCF=0x00C [Success]
144   2026-01-14-00-01-17.157127   73189.26     Controller->Host   EVENT        -      -      0x32 Event_0x32
145   2026-01-14-00-01-17.157425   73189.56     Controller->Host   EVENT        -      -      0x31 Event_0x31
146   2026-01-14-00-01-17.157700   73189.83     Host->Controller   CMD          0x01   0x02B  0x042B OGF=0x01, OCF=0x02B
147   2026-01-14-00-01-17.159218   73191.35     Controller->Host   EVENT        0x01   0x02B  0x0E Command Complete -> OGF=0x01, OCF=0x02B [Success]
148   2026-01-14-00-01-17.262260   73294.40     Controller->Host   EVENT        -      -      0x33 Event_0x33
149   2026-01-14-00-01-17.262657   73294.79     Host->Controller   CMD          0x01   0x02C  0x042C OGF=0x01, OCF=0x02C
150   2026-01-14-00-01-17.264030   73296.16     Controller->Host   EVENT        0x01   0x02C  0x0E Command Complete -> OGF=0x01, OCF=0x02C [Success]
151   2026-01-14-00-01-17.563759   73595.89     Controller->Host   EVENT        -      -      0x36 Event_0x36
152   2026-01-14-00-01-17.574883   73607.01     Controller->Host   EVENT        -      -      0x18 Event_0x18
153   2026-01-14-00-01-17.581673   73613.80     Host->Controller   CMD          0x03   0x07D  0x0C7D Read Local OOB Extended Data
154   2026-01-14-00-01-17.588905   73621.03     Controller->Host   EVENT        0x03   0x07D  0x0E Command Complete -> Read Local OOB Extended Data [Success]
155   2026-01-14-00-01-17.604126   73636.26     Controller->Host   EVENT        -      -      0x08 Event_0x08
156   2026-01-14-00-01-17.610893   73643.02     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
157   2026-01-14-00-01-17.612495   73644.63     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
158   2026-01-14-00-01-17.615097   73647.23     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
159   2026-01-14-00-01-17.622223   73654.35     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
160   2026-01-14-00-01-17.623634   73655.76     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
161   2026-01-14-00-01-17.623810   73655.94     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
162   2026-01-14-00-01-17.623848   73655.98     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
163   2026-01-14-00-01-17.630959   73663.09     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
164   2026-01-14-00-01-17.632385   73664.52     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
165   2026-01-14-00-01-17.632645   73664.78     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
166   2026-01-14-00-01-17.635078   73667.21     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
167   2026-01-14-00-01-17.636269   73668.41     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
168   2026-01-14-00-01-17.640167   73672.30     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
169   2026-01-14-00-01-17.640419   73672.55     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
170   2026-01-14-00-01-17.649628   73681.76     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
171   2026-01-14-00-01-17.655762   73687.90     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
172   2026-01-14-00-01-17.656784   73688.91     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
173   2026-01-14-00-01-17.661453   73693.59     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
174   2026-01-14-00-01-17.665878   73698.01     Host->Controller   CMD          0x08   0x00A  0x200A LE Set Advertising Enable
175   2026-01-14-00-01-17.670609   73702.74     Controller->Host   EVENT        0x08   0x00A  0x0E Command Complete -> LE Set Advertising Enable [Success]
176   2026-01-14-00-01-17.673660   73705.80     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
177   2026-01-14-00-01-17.675041   73707.18     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
178   2026-01-14-00-01-17.677216   73709.35     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
179   2026-01-14-00-01-17.677696   73709.83     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
180   2026-01-14-00-01-17.677773   73709.91     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
181   2026-01-14-00-01-17.682037   73714.17     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
182   2026-01-14-00-01-17.683464   73715.60     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
183   2026-01-14-00-01-17.684639   73716.77     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
184   2026-01-14-00-01-17.723740   73755.87     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
185   2026-01-14-00-01-17.730995   73763.12     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
186   2026-01-14-00-01-17.734581   73766.72     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
187   2026-01-14-00-01-17.740700   73772.83     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
188   2026-01-14-00-01-17.745628   73777.76     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
189   2026-01-14-00-01-17.758469   73790.60     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
190   2026-01-14-00-01-17.775665   73807.79     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
191   2026-01-14-00-01-17.775795   73807.92     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
192   2026-01-14-00-01-17.780830   73812.96     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
193   2026-01-14-00-01-17.783150   73815.29     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
194   2026-01-14-00-01-17.783821   73815.96     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
195   2026-01-14-00-01-17.785591   73817.73     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
196   2026-01-14-00-01-17.815826   73847.96     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
197   2026-01-14-00-01-17.816994   73849.12     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
198   2026-01-14-00-01-17.819489   73851.62     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
199   2026-01-14-00-01-17.819954   73852.08     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
200   2026-01-14-00-01-17.820015   73852.15     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
201   2026-01-14-00-01-17.829506   73861.63     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
202   2026-01-14-00-01-17.832085   73864.22     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
203   2026-01-14-00-01-17.833321   73865.45     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
204   2026-01-14-00-01-17.839165   73871.30     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
205   2026-01-14-00-01-17.846001   73878.13     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
206   2026-01-14-00-01-17.850830   73882.96     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
207   2026-01-14-00-01-17.869392   73901.52     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
208   2026-01-14-00-01-17.896317   73928.45     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
209   2026-01-14-00-01-17.912201   73944.34     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
210   2026-01-14-00-01-17.978065   74010.20     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
211   2026-01-14-00-01-17.984596   74016.73     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
212   2026-01-14-00-01-17.995880   74028.01     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
213   2026-01-14-00-01-18.010384   74042.52     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
214   2026-01-14-00-01-18.016136   74048.27     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
215   2026-01-14-00-01-18.028435   74060.57     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
216   2026-01-14-00-01-18.038200   74070.33     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
217   2026-01-14-00-01-18.044617   74076.74     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
218   2026-01-14-00-01-18.059792   74091.92     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
219   2026-01-14-00-01-22.348770   78380.90     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
220   2026-01-14-00-01-22.380325   78412.46     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
221   2026-01-14-00-01-22.380432   78412.57     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
222   2026-01-14-00-01-22.405823   78437.95     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
223   2026-01-14-00-01-22.407005   78439.14     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
224   2026-01-14-00-01-22.436974   78469.10     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
225   2026-01-14-00-01-22.439255   78471.39     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
226   2026-01-14-00-01-22.459335   78491.47     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
227   2026-01-14-00-01-22.469551   78501.68     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
228   2026-01-14-00-01-22.522026   78554.16     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
229   2026-01-14-00-01-22.523613   78555.75     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
230   2026-01-14-00-01-22.528442   78560.57     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
231   2026-01-14-00-01-22.553322   78585.46     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
232   2026-01-14-00-01-23.434448   79466.58     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
233   2026-01-14-00-01-23.438713   79470.84     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
234   2026-01-14-00-01-23.464539   79496.67     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
235   2026-01-14-00-01-23.469406   79501.54     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
236   2026-01-14-00-01-23.473701   79505.83     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
237   2026-01-14-00-01-23.499542   79531.68     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
238   2026-01-14-00-01-23.501953   79534.08     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
239   2026-01-14-00-01-23.640335   79672.47     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
240   2026-01-14-00-01-23.659119   79691.25     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
241   2026-01-14-00-01-25.448654   81480.79     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
242   2026-01-14-00-01-25.483299   81515.43     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
243   2026-01-14-00-01-25.491371   81523.50     Host->Controller   CMD          0x08   0x00A  0x200A LE Set Advertising Enable
244   2026-01-14-00-01-25.493210   81525.34     Controller->Host   EVENT        0x08   0x00A  0x0E Command Complete -> LE Set Advertising Enable [Success]
245   2026-01-14-00-01-25.499405   81531.54     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
246   2026-01-14-00-01-25.615585   81647.72     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
247   2026-01-14-00-01-25.615837   81647.97     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
248   2026-01-14-00-01-25.622719   81654.85     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
249   2026-01-14-00-01-25.624275   81656.40     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
250   2026-01-14-00-01-25.624687   81656.82     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x004D,Dynamic_CID_0x004D)
251   2026-01-14-00-01-25.653252   81685.38     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
252   2026-01-14-00-01-25.654411   81686.54     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
253   2026-01-14-00-01-25.655670   81687.81     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
254   2026-01-14-00-01-25.684708   81716.84     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
255   2026-01-14-00-01-29.716896   85749.03     Controller->Host   EVENT        -      -      0x05 Disconnection Complete
256   2026-01-14-00-01-40.013062   96045.20     Controller->Host   EVENT        -      -      0x04 Connection Request
257   2026-01-14-00-01-40.013466   96045.60     Host->Controller   CMD          0x01   0x009  0x0409 Accept Connection Request
258   2026-01-14-00-01-40.016273   96048.41     Controller->Host   EVENT        -      -      0x0F Command Status
259   2026-01-14-00-01-40.035789   96067.92     Controller->Host   EVENT        -      -      0x20 Page Scan Repetition Mode Change
260   2026-01-14-00-01-40.036560   96068.70     Controller->Host   EVENT        -      -      0x03 Connection Complete Handle=0x0001 Addr=A8:6E:4E:43:F3:B9
261   2026-01-14-00-01-40.037048   96069.18     Host->Controller   CMD          0x01   0x00F  0x040F Change Connection Packet Type
262   2026-01-14-00-01-40.037117   96069.25     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
263   2026-01-14-00-01-40.038528   96070.66     Controller->Host   EVENT        -      -      0x0F Command Status
264   2026-01-14-00-01-40.038628   96070.76     Host->Controller   CMD          0x02   0x009  0x0809 OGF=0x02, OCF=0x009
265   2026-01-14-00-01-40.040039   96072.17     Controller->Host   EVENT        0x02   0x009  0x0E Command Complete -> OGF=0x02, OCF=0x009 [Success]
266   2026-01-14-00-01-40.040260   96072.39     Host->Controller   CMD          0x02   0x00D  0x080D Exit Sniff Mode
267   2026-01-14-00-01-40.041618   96073.75     Controller->Host   EVENT        0x02   0x00D  0x0E Command Complete -> Exit Sniff Mode [Success]
268   2026-01-14-00-01-40.041893   96074.03     Host->Controller   CMD          0x01   0x01B  0x041B OGF=0x01, OCF=0x01B
269   2026-01-14-00-01-40.043320   96075.45     Controller->Host   EVENT        -      -      0x0F Command Status
270   2026-01-14-00-01-40.043434   96075.56     Host->Controller   CMD          0x01   0x019  0x0419 Remote Name Request
271   2026-01-14-00-01-40.044792   96076.93     Controller->Host   EVENT        -      -      0x0F Command Status
272   2026-01-14-00-01-40.111748   96143.88     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
273   2026-01-14-00-01-40.111877   96144.01     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
274   2026-01-14-00-01-40.113190   96145.32     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
275   2026-01-14-00-01-40.113304   96145.43     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
276   2026-01-14-00-01-40.114548   96146.67     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
277   2026-01-14-00-01-40.114632   96146.76     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
278   2026-01-14-00-01-40.120148   96152.28     Controller->Host   EVENT        -      -      0x1B Event_0x1B
279   2026-01-14-00-01-40.121857   96153.98     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
280   2026-01-14-00-01-40.124847   96156.98     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
281   2026-01-14-00-01-40.126938   96159.07     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
282   2026-01-14-00-01-40.127144   96159.28     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
283   2026-01-14-00-01-40.127190   96159.33     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
284   2026-01-14-00-01-40.128937   96161.07     Controller->Host   EVENT        -      -      0x07 Event_0x07
285   2026-01-14-00-01-40.129379   96161.51     Controller->Host   EVENT        -      -      0x1D Event_0x1D
286   2026-01-14-00-01-40.129486   96161.62     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
287   2026-01-14-00-01-40.129585   96161.72     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
288   2026-01-14-00-01-40.130829   96162.97     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
289   2026-01-14-00-01-40.131989   96164.12     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
290   2026-01-14-00-01-40.133438   96165.57     Controller->Host   EVENT        -      -      0x0B Event_0x0B
291   2026-01-14-00-01-40.133827   96165.95     Controller->Host   EVENT        -      -      0x38 Event_0x38
292   2026-01-14-00-01-40.133919   96166.05     Host->Controller   CMD          0x01   0x01C  0x041C OGF=0x01, OCF=0x01C
293   2026-01-14-00-01-40.135345   96167.47     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
294   2026-01-14-00-01-40.135391   96167.52     Controller->Host   EVENT        -      -      0x0F Command Status
295   2026-01-14-00-01-40.135445   96167.58     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
296   2026-01-14-00-01-40.138382   96170.52     Controller->Host   EVENT        -      -      0x23 Event_0x23
297   2026-01-14-00-01-40.138657   96170.78     Controller->Host   EVENT        -      -      0x32 Event_0x32
298   2026-01-14-00-01-40.138680   96170.81     Controller->Host   EVENT        -      -      0x31 Event_0x31
299   2026-01-14-00-01-40.138802   96170.94     Host->Controller   CMD          0x01   0x02B  0x042B OGF=0x01, OCF=0x02B
300   2026-01-14-00-01-40.140228   96172.36     Controller->Host   EVENT        0x01   0x02B  0x0E Command Complete -> OGF=0x01, OCF=0x02B [Success]
301   2026-01-14-00-01-40.220856   96252.99     Controller->Host   EVENT        -      -      0x33 Event_0x33
302   2026-01-14-00-01-40.227440   96259.57     Host->Controller   CMD          0x01   0x02C  0x042C OGF=0x01, OCF=0x02C
303   2026-01-14-00-01-40.230164   96262.29     Controller->Host   EVENT        0x01   0x02C  0x0E Command Complete -> OGF=0x01, OCF=0x02C [Success]
304   2026-01-14-00-01-40.471077   96503.21     Controller->Host   EVENT        -      -      0x36 Event_0x36
305   2026-01-14-00-01-40.481888   96514.02     Controller->Host   EVENT        -      -      0x18 Event_0x18
306   2026-01-14-00-01-40.484711   96516.84     Host->Controller   CMD          0x03   0x07D  0x0C7D Read Local OOB Extended Data
307   2026-01-14-00-01-40.487335   96519.47     Controller->Host   EVENT        0x03   0x07D  0x0E Command Complete -> Read Local OOB Extended Data [Success]
308   2026-01-14-00-01-40.524361   96556.49     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
309   2026-01-14-00-01-40.524864   96557.00     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
310   2026-01-14-00-01-40.526131   96558.26     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
311   2026-01-14-00-01-40.529846   96561.98     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
312   2026-01-14-00-01-40.531021   96563.16     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
313   2026-01-14-00-01-40.531158   96563.29     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
314   2026-01-14-00-01-40.531189   96563.32     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
315   2026-01-14-00-01-40.534271   96566.41     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
316   2026-01-14-00-01-40.535690   96567.82     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
317   2026-01-14-00-01-40.539207   96571.34     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
318   2026-01-14-00-01-40.539574   96571.71     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0051,Dynamic_CID_0x0051)
319   2026-01-14-00-01-40.544838   96576.97     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
320   2026-01-14-00-01-40.546738   96578.87     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
321   2026-01-14-00-01-40.549263   96581.40     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
322   2026-01-14-00-01-40.564850   96596.98     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
323   2026-01-14-00-01-40.566833   96598.97     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
324   2026-01-14-00-01-40.567398   96599.53     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
325   2026-01-14-00-01-40.568672   96600.81     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
326   2026-01-14-00-01-40.584869   96617.00     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
327   2026-01-14-00-01-40.586060   96618.19     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
328   2026-01-14-00-01-40.586182   96618.32     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
329   2026-01-14-00-01-40.586220   96618.35     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
330   2026-01-14-00-01-40.589539   96621.67     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
331   2026-01-14-00-01-40.591095   96623.23     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
332   2026-01-14-00-01-40.592979   96625.11     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
333   2026-01-14-00-01-40.593407   96625.54     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
334   2026-01-14-00-01-40.598114   96630.25     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
335   2026-01-14-00-01-40.601059   96633.19     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
336   2026-01-14-00-01-40.601372   96633.50     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
337   2026-01-14-00-01-40.618866   96650.99     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
338   2026-01-14-00-01-40.621849   96653.98     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
339   2026-01-14-00-01-40.622223   96654.36     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
340   2026-01-14-00-01-40.627930   96660.06     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
341   2026-01-14-00-01-40.630470   96662.61     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
342   2026-01-14-00-01-40.630791   96662.93     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
343   2026-01-14-00-01-40.635681   96667.81     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
344   2026-01-14-00-01-40.639839   96671.97     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
345   2026-01-14-00-01-40.640190   96672.32     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
346   2026-01-14-00-01-40.656883   96689.01     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
347   2026-01-14-00-01-40.661629   96693.76     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
348   2026-01-14-00-01-40.661942   96694.08     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
349   2026-01-14-00-01-40.695648   96727.78     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
350   2026-01-14-00-01-40.698090   96730.22     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
351   2026-01-14-00-01-40.698341   96730.47     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
352   2026-01-14-00-01-40.703217   96735.35     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
353   2026-01-14-00-01-40.705391   96737.53     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
354   2026-01-14-00-01-40.705658   96737.79     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
355   2026-01-14-00-01-40.719872   96752.00     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
356   2026-01-14-00-01-40.724564   96756.69     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
357   2026-01-14-00-01-40.724899   96757.03     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
358   2026-01-14-00-01-40.741928   96774.06     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
359   2026-01-14-00-01-40.746796   96778.92     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
360   2026-01-14-00-01-40.747131   96779.26     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
361   2026-01-14-00-01-40.752007   96784.14     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
362   2026-01-14-00-01-40.759239   96791.37     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
363   2026-01-14-00-01-40.759483   96791.61     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0050,Dynamic_CID_0x0050)
364   2026-01-14-00-01-40.764771   96796.90     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
365   2026-01-14-00-01-40.766830   96798.97     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
366   2026-01-14-00-01-40.768234   96800.36     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
367   2026-01-14-00-01-40.784882   96817.01     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
368   2026-01-14-00-01-40.840561   96872.69     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
369   2026-01-14-00-01-40.841171   96873.30     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
370   2026-01-14-00-01-40.842499   96874.63     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
371   2026-01-14-00-01-40.858185   96890.32     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
372   2026-01-14-00-01-40.860016   96892.15     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
373   2026-01-14-00-01-40.861237   96893.37     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
374   2026-01-14-00-01-40.861427   96893.55     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
375   2026-01-14-00-01-40.864311   96896.45     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
376   2026-01-14-00-01-40.865822   96897.96     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
377   2026-01-14-00-01-40.869919   96902.06     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
378   2026-01-14-00-01-40.870399   96902.53     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0053,Dynamic_CID_0x0053)
379   2026-01-14-00-01-40.886978   96919.11     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
380   2026-01-14-00-01-40.888168   96920.30     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
381   2026-01-14-00-01-40.889587   96921.71     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
382   2026-01-14-00-01-40.905670   96937.81     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
383   2026-01-14-00-01-40.920860   96952.99     Controller->Host   EVENT        -      -      0x08 Event_0x08
384   2026-01-14-00-01-40.925529   96957.66     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
385   2026-01-14-00-01-40.925926   96958.06     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
386   2026-01-14-00-01-40.927650   96959.78     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
387   2026-01-14-00-01-40.931412   96963.54     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
388   2026-01-14-00-01-40.932610   96964.74     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
389   2026-01-14-00-01-40.932793   96964.93     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
390   2026-01-14-00-01-40.932838   96964.97     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
391   2026-01-14-00-01-40.938072   96970.20     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
392   2026-01-14-00-01-40.939453   96971.59     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
393   2026-01-14-00-01-40.939507   96971.64     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
394   2026-01-14-00-01-40.939606   96971.74     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
395   2026-01-14-00-01-40.944801   96976.93     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
396   2026-01-14-00-01-40.946030   96978.16     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
397   2026-01-14-00-01-40.946198   96978.33     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
398   2026-01-14-00-01-40.963165   96995.30     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
399   2026-01-14-00-01-40.964340   96996.47     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
400   2026-01-14-00-01-40.968407   97000.54     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
401   2026-01-14-00-01-40.968506   97000.63     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
402   2026-01-14-00-01-40.968552   97000.68     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
403   2026-01-14-00-01-40.981873   97014.01     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
404   2026-01-14-00-01-40.983154   97015.29     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
405   2026-01-14-00-01-40.984390   97016.52     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
406   2026-01-14-00-01-40.985695   97017.83     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
407   2026-01-14-00-01-40.985794   97017.92     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
408   2026-01-14-00-01-40.985817   97017.95     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
409   2026-01-14-00-01-40.987160   97019.29     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
410   2026-01-14-00-01-41.009384   97041.52     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
411   2026-01-14-00-01-41.009552   97041.68     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
412   2026-01-14-00-01-41.010727   97042.86     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
413   2026-01-14-00-01-41.010902   97043.03     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
414   2026-01-14-00-01-41.012054   97044.19     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
415   2026-01-14-00-01-41.013268   97045.40     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
416   2026-01-14-00-01-41.018517   97050.65     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
417   2026-01-14-00-01-41.019073   97051.21     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0055,Dynamic_CID_0x0055)
418   2026-01-14-00-01-41.035660   97067.79     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
419   2026-01-14-00-01-41.039207   97071.34     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0041,Dynamic_CID_0x0041)
420   2026-01-14-00-01-41.040909   97073.05     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
421   2026-01-14-00-01-41.044861   97077.00     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
422   2026-01-14-00-01-41.048019   97080.15     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
423   2026-01-14-00-01-41.090919   97123.05     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
424   2026-01-14-00-01-41.093353   97125.48     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
425   2026-01-14-00-01-41.098572   97130.70     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
426   2026-01-14-00-01-41.099442   97131.57     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
427   2026-01-14-00-01-41.100044   97132.18     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
428   2026-01-14-00-01-41.115685   97147.82     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
429   2026-01-14-00-01-41.119286   97151.42     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
430   2026-01-14-00-01-41.119904   97152.03     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
431   2026-01-14-00-01-41.134972   97167.10     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
432   2026-01-14-00-01-41.140961   97173.09     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
433   2026-01-14-00-01-41.142975   97175.11     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
434   2026-01-14-00-01-41.143280   97175.41     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
435   2026-01-14-00-01-41.150696   97182.83     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
436   2026-01-14-00-01-41.153069   97185.21     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
437   2026-01-14-00-01-41.155090   97187.22     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
438   2026-01-14-00-01-41.155617   97187.75     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
439   2026-01-14-00-01-41.171898   97204.03     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
440   2026-01-14-00-01-41.174217   97206.35     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
441   2026-01-14-00-01-41.174622   97206.76     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
442   2026-01-14-00-01-41.179840   97211.97     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
443   2026-01-14-00-01-41.181709   97213.84     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
444   2026-01-14-00-01-41.183250   97215.38     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
445   2026-01-14-00-01-41.184410   97216.54     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
446   2026-01-14-00-01-41.200638   97232.77     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
447   2026-01-14-00-01-41.208221   97240.36     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
448   2026-01-14-00-01-41.212822   97244.95     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
449   2026-01-14-00-01-41.225624   97257.76     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
450   2026-01-14-00-01-41.226898   97259.03     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
451   2026-01-14-00-01-41.227760   97259.89     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
452   2026-01-14-00-01-41.244865   97277.00     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
453   2026-01-14-00-01-41.247154   97279.28     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
454   2026-01-14-00-01-41.247772   97279.91     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
455   2026-01-14-00-01-41.249985   97282.12     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
456   2026-01-14-00-01-41.263771   97295.90     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
457   2026-01-14-00-01-41.264961   97297.09     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
458   2026-01-14-00-01-41.265015   97297.15     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
459   2026-01-14-00-01-41.265594   97297.72     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
460   2026-01-14-00-01-41.268333   97300.47     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
461   2026-01-14-00-01-41.270653   97302.79     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
462   2026-01-14-00-01-41.272011   97304.14     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
463   2026-01-14-00-01-41.272118   97304.26     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
464   2026-01-14-00-01-41.272186   97304.32     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
465   2026-01-14-00-01-41.273773   97305.90     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
466   2026-01-14-00-01-41.274437   97306.57     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
467   2026-01-14-00-01-41.275726   97307.86     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
468   2026-01-14-00-01-41.275780   97307.91     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
469   2026-01-14-00-01-41.276894   97309.02     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
470   2026-01-14-00-01-41.279686   97311.82     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
471   2026-01-14-00-01-41.280045   97312.18     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0054,Dynamic_CID_0x0054)
472   2026-01-14-00-01-41.304443   97336.57     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
473   2026-01-14-00-01-41.305206   97337.34     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
474   2026-01-14-00-01-41.306465   97338.60     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
475   2026-01-14-00-01-41.309128   97341.26     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
476   2026-01-14-00-01-41.317955   97350.09     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0041,Dynamic_CID_0x0041)
477   2026-01-14-00-01-41.319733   97351.87     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
478   2026-01-14-00-01-41.319832   97351.97     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
479   2026-01-14-00-01-41.319855   97351.99     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
480   2026-01-14-00-01-41.320335   97352.47     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
481   2026-01-14-00-01-41.324936   97357.07     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
482   2026-01-14-00-01-41.326088   97358.22     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
483   2026-01-14-00-01-41.326118   97358.25     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
484   2026-01-14-00-01-41.327591   97359.73     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
485   2026-01-14-00-01-41.331467   97363.60     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
486   2026-01-14-00-01-41.331871   97364.00     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
487   2026-01-14-00-01-41.332306   97364.44     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
488   2026-01-14-00-01-41.332382   97364.51     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
489   2026-01-14-00-01-41.336861   97368.99     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
490   2026-01-14-00-01-41.338158   97370.29     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
491   2026-01-14-00-01-41.339279   97371.41     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
492   2026-01-14-00-01-41.340096   97372.23     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
493   2026-01-14-00-01-41.356735   97388.87     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
494   2026-01-14-00-01-41.358421   97390.55     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
495   2026-01-14-00-01-41.358513   97390.65     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
496   2026-01-14-00-01-41.372978   97405.11     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
497   2026-01-14-00-01-41.374161   97406.29     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
498   2026-01-14-00-01-41.374275   97406.40     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
499   2026-01-14-00-01-41.374313   97406.44     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
500   2026-01-14-00-01-41.375626   97407.76     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
501   2026-01-14-00-01-41.379875   97412.00     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
502   2026-01-14-00-01-41.381050   97413.18     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
503   2026-01-14-00-01-41.381744   97413.88     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
504   2026-01-14-00-01-41.383148   97415.29     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
505   2026-01-14-00-01-43.781807   99813.94     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
506   2026-01-14-00-01-43.791908   99824.04     Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
507   2026-01-14-00-01-43.800461   99832.60     Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
508   2026-01-14-00-01-48.118248   104150.38    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
509   2026-01-14-00-01-48.140823   104172.96    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
510   2026-01-14-00-01-48.150795   104182.93    Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
511   2026-01-14-00-01-48.167877   104200.01    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
512   2026-01-14-00-01-48.171227   104203.36    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
513   2026-01-14-00-01-48.198158   104230.29    Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
514   2026-01-14-00-01-48.209206   104241.34    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
515   2026-01-14-00-01-55.226295   111258.43    Controller->Host   EVENT        -      -      0x14 Event_0x14
516   2026-01-14-00-02-48.140045   164172.18    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
517   2026-01-14-00-02-48.261230   164293.36    Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
518   2026-01-14-00-02-48.758354   164790.49    Controller->Host   EVENT        -      -      0x14 Event_0x14
519   2026-01-14-00-02-48.761002   164793.13    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
520   2026-01-14-00-02-48.966095   164998.22    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
521   2026-01-14-00-02-48.973709   165005.84    Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
522   2026-01-14-00-02-48.984749   165016.89    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
523   2026-01-14-00-02-49.198692   165230.83    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
524   2026-01-14-00-02-49.222588   165254.72    Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
525   2026-01-14-00-02-49.249741   165281.88    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
526   2026-01-14-00-02-49.460915   165493.04    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
527   2026-01-14-00-02-49.486641   165518.77    Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
528   2026-01-14-00-02-49.497215   165529.35    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
529   2026-01-14-00-02-49.500259   165532.39    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0052,Dynamic_CID_0x0052)
530   2026-01-14-00-02-49.527534   165559.66    Controller->Host   EVENT        -      -      0x13 Number of Completed Packets
531   2026-01-14-00-02-49.556137   165588.27    Host->Controller   ACL_DATA     -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
532   2026-01-14-00-02-56.550667   172582.80    Controller->Host   EVENT        -      -      0x14 Event_0x14
```

## 📝 分析总结

1. **连接管理**: 2 个连接建立，1 个断开

2. **数据传输**: 246 个 ACL 数据包，句柄 0x0001

3. **错误状态**: 未发现 HCI 层错误

---

**架构**: BTSnoop → HCI(命令/事件/ACL) → L2CAP(信令/ATT) → 可扩展 SDP 等
