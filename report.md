# BTSnoop HCI 日志解析报告

> 分层: HCI 命令/事件/ACL → L2CAP 信令/ATT

## 📊 概览统计

- **文件**: `examples/sample_hci.log`
- **总数据包**: 532
- **持续时间**: 172582.80 ms
- **HCI 命令**: 121 | **HCI 事件**: 221
- **ACL TX**: 125 | **ACL RX**: 0
- **错误数**: 0
- **连接句柄**: 0x0001

## ✅ Command Complete 验证

| 序号 | 时间(ms) | 命令 | OGF | OCF | 状态 |
|------|----------|------|-----|-----|------|
| 2 | 95.23 | Reset | 0x03 | 0x003 | Success |
| 4 | 102.16 | Read Buffer Size | 0x04 | 0x005 | Success |
| 6 | 109.28 | Host Buffer Size | 0x03 | 0x033 | Success |
| 8 | 113.72 | Read Local Supported Features | 0x04 | 0x003 | Success |
| 10 | 118.15 | Write LE Host Supported | 0x03 | 0x06D | Success |
| 12 | 126.75 | LE Read Buffer Size | 0x08 | 0x002 | Success |
| 14 | 130.60 | Read Local Extended Features | 0x04 | 0x004 | Success |
| 16 | 136.36 | Write Page Timeout | 0x03 | 0x018 | Success |
| 18 | 140.34 | Read Page Timeout | 0x03 | 0x017 | Success |
| 20 | 144.02 | Set Event Mask | 0x03 | 0x001 | Success |

... 共 55 个

## 🔗 连接建立事件

| 序号 | 时间(ms) | 句柄 | 设备地址 | 状态 |
|------|----------|------|----------|------|
| 89 | 73023.75 | 0x0001 | A8:6E:4E:43:F3:B9 | Success |
| 260 | 96068.70 | 0x0001 | A8:6E:4E:43:F3:B9 | Success |

## 🔴 断开连接事件

| 序号 | 时间(ms) | 句柄 | 原因 |
|------|----------|------|------|
| 255 | 85749.03 | 0x0001 | Remote User Terminated Connection |

## 📋 详细通信流程

```
#     Delta(ms)    Direction          Type         OGF    OCF    Details
----------------------------------------------------------------------------------------------------
1     0.00         Host->Controller   CMD          0x03   0x003  0x0C03 Reset
2     95.23        Controller->Host   EVT          0x03   0x003  0x0E Command Complete -> Reset [Success]
3     95.51        Host->Controller   CMD          0x04   0x005  0x1005 Read Buffer Size
4     102.16       Controller->Host   EVT          0x04   0x005  0x0E Command Complete -> Read Buffer Size [Success]
5     102.46       Host->Controller   CMD          0x03   0x033  0x0C33 Host Buffer Size
6     109.28       Controller->Host   EVT          0x03   0x033  0x0E Command Complete -> Host Buffer Size [Success]
7     109.56       Host->Controller   CMD          0x04   0x003  0x1003 Read Local Supported Features
8     113.72       Controller->Host   EVT          0x04   0x003  0x0E Command Complete -> Read Local Supported Features [Success]
9     113.96       Host->Controller   CMD          0x03   0x06D  0x0C6D Write LE Host Supported
10    118.15       Controller->Host   EVT          0x03   0x06D  0x0E Command Complete -> Write LE Host Supported [Success]
11    118.40       Host->Controller   CMD          0x08   0x002  0x2002 LE Read Buffer Size
12    126.75       Controller->Host   EVT          0x08   0x002  0x0E Command Complete -> LE Read Buffer Size [Success]
13    127.14       Host->Controller   CMD          0x04   0x004  0x1004 Read Local Extended Features
14    130.60       Controller->Host   EVT          0x04   0x004  0x0E Command Complete -> Read Local Extended Features [Success]
15    131.32       Host->Controller   CMD          0x03   0x018  0x0C18 Write Page Timeout
16    136.36       Controller->Host   EVT          0x03   0x018  0x0E Command Complete -> Write Page Timeout [Success]
17    136.73       Host->Controller   CMD          0x03   0x017  0x0C17 Read Page Timeout
18    140.34       Controller->Host   EVT          0x03   0x017  0x0E Command Complete -> Read Page Timeout [Success]
19    140.62       Host->Controller   CMD          0x03   0x001  0x0C01 Set Event Mask
20    144.02       Controller->Host   EVT          0x03   0x001  0x0E Command Complete -> Set Event Mask [Success]
21    144.43       Host->Controller   CMD          0x04   0x001  0x1001 Read Local Version Information
22    151.16       Controller->Host   EVT          0x04   0x001  0x0E Command Complete -> Read Local Version Information [Success]
23    151.34       Host->Controller   CMD          0x04   0x009  0x1009 Read BD_ADDR
24    155.44       Controller->Host   EVT          0x04   0x009  0x0E Command Complete -> Read BD_ADDR [Success]
25    155.69       Host->Controller   CMD          0x03   0x044  0x0C44 Read Inquiry Mode
26    161.68       Controller->Host   EVT          0x03   0x044  0x0E Command Complete -> Read Inquiry Mode [Success]
27    162.03       Host->Controller   CMD          0x03   0x05A  0x0C5A Read Default Erroneous Data Reporting
28    166.48       Controller->Host   EVT          0x03   0x05A  0x0E Command Complete -> Read Default Erroneous Data Reporting [Success]
29    166.70       Host->Controller   CMD          0x03   0x058  0x0C58 Read Inquiry Response Transmit Power Level
30    172.70       Controller->Host   EVT          0x03   0x058  0x0E Command Complete -> Read Inquiry Response Transmit Power Level [Success]
31    172.93       Host->Controller   CMD          0x03   0x056  0x0C56 Write Simple Pairing Mode
32    182.96       Controller->Host   EVT          0x03   0x056  0x0E Command Complete -> Write Simple Pairing Mode [Success]
33    183.24       Host->Controller   CMD          0x08   0x001  0x2001 LE Set Event Mask
34    190.99       Controller->Host   EVT          0x08   0x001  0x0E Command Complete -> LE Set Event Mask [Success]
35    191.21       Host->Controller   CMD          0x08   0x003  0x2003 LE Read Local Supported Features Page 0
36    195.87       Controller->Host   EVT          0x08   0x003  0x0E Command Complete -> LE Read Local Supported Features Page 0 [Success]
37    196.10       Host->Controller   CMD          0x08   0x007  0x2007 LE Read Advertising Channel TX Power
38    202.42       Controller->Host   EVT          0x08   0x007  0x0E Command Complete -> LE Read Advertising Channel TX Power [Success]
39    202.70       Host->Controller   CMD          0x08   0x01C  0x201C LE Read Supported States
40    206.75       Controller->Host   EVT          0x08   0x01C  0x0E Command Complete -> LE Read Supported States [Success]
41    207.05       Host->Controller   CMD          0x08   0x00F  0x200F LE Read Filter Accept List Size
42    212.16       Controller->Host   EVT          0x08   0x00F  0x0E Command Complete -> LE Read Filter Accept List Size [Success]
43    266.39       Host->Controller   CMD          0x02   0x00F  0x080F Write Default Link Policy Settings
44    271.42       Controller->Host   EVT          0x02   0x00F  0x0E Command Complete -> Write Default Link Policy Settings [Success]
45    271.66       Host->Controller   CMD          0x03   0x045  0x0C45 Write Inquiry Mode
46    276.20       Controller->Host   EVT          0x03   0x045  0x0E Command Complete -> Write Inquiry Mode [Success]
47    276.51       Host->Controller   CMD          0x03   0x01C  0x0C1C Write Page Scan Activity
48    280.06       Controller->Host   EVT          0x03   0x01C  0x0E Command Complete -> Write Page Scan Activity [Success]
49    280.32       Host->Controller   CMD          0x03   0x01E  0x0C1E Write Inqury Scan Activity
50    288.31       Controller->Host   EVT          0x03   0x01E  0x0E Command Complete -> Write Inqury Scan Activity [Success]
51    288.81       Host->Controller   CMD          0x03   0x01A  0x0C1A Write Scan Enable
52    297.40       Controller->Host   EVT          0x03   0x01A  0x0E Command Complete -> Write Scan Enable [Success]
53    297.86       Host->Controller   CMD          0x03   0x024  0x0C24 Write Class of Device
54    309.16       Controller->Host   EVT          0x03   0x024  0x0E Command Complete -> Write Class of Device [Success]
55    309.41       Host->Controller   CMD          0x08   0x008  0x2008 LE Set Advertising Data
56    316.21       Controller->Host   EVT          0x08   0x008  0x0E Command Complete -> LE Set Advertising Data [Success]
57    316.46       Host->Controller   CMD          0x03   0x013  0x0C13 Write Local Name
58    320.02       Controller->Host   EVT          0x03   0x013  0x0E Command Complete -> Write Local Name [Success]
59    320.11       Host->Controller   CMD          0x3F   0x01D  0xFC1D Vendor Command 0x01D
60    326.02       Controller->Host   EVT          0x3F   0x01D  0x0E Command Complete -> Vendor Command 0x01D [Success]
61    326.30       Host->Controller   CMD          0x03   0x052  0x0C52 Write Extended Inqury Response
62    357.54       Controller->Host   EVT          0x03   0x052  0x0E Command Complete -> Write Extended Inqury Response [Success]
63    357.75       Host->Controller   CMD          0x3F   0x007  0xFC07 Vendor Command 0x007
64    359.26       Controller->Host   EVT          0x3F   0x007  0x0E Command Complete -> Vendor Command 0x007 [Success]
65    359.39       Host->Controller   CMD          0x3F   0x028  0xFC28 Vendor Command 0x028
66    361.93       Controller->Host   EVT          0x3F   0x028  0x0E Command Complete -> Vendor Command 0x028 [Success]
67    362.13       Host->Controller   CMD          0x3F   0x029  0xFC29 Vendor Command 0x029
68    380.98       Controller->Host   EVT          0x3F   0x029  0x0E Command Complete -> Vendor Command 0x029 [Success]
69    381.16       Host->Controller   CMD          0x3F   0x073  0xFC73 Vendor Command 0x073
70    387.09       Controller->Host   EVT          0x3F   0x073  0x0E Command Complete -> Vendor Command 0x073 [Success]
71    387.36       Host->Controller   CMD          0x03   0x07D  0x0C7D Read Local OOB Extended Data
72    393.52       Controller->Host   EVT          0x03   0x07D  0x0E Command Complete -> Read Local OOB Extended Data [Success]
73    393.98       Host->Controller   CMD          0x03   0x07A  0x0C7A Write Secure Connections Host Support
74    399.51       Controller->Host   EVT          0x03   0x07A  0x0E Command Complete -> Write Secure Connections Host Support [Success]
75    5225.47      Host->Controller   CMD          0x03   0x01A  0x0C1A Write Scan Enable
76    5257.41      Controller->Host   EVT          0x03   0x01A  0x0E Command Complete -> Write Scan Enable [Success]
77    70239.04     Host->Controller   CMD          0x03   0x01A  0x0C1A Write Scan Enable
78    70270.33     Controller->Host   EVT          0x03   0x01A  0x0E Command Complete -> Write Scan Enable [Success]
79    70270.78     Host->Controller   CMD          0x08   0x006  0x2006 LE Set Advertising Parameters
80    70272.18     Controller->Host   EVT          0x08   0x006  0x0E Command Complete -> LE Set Advertising Parameters [Success]
81    70272.38     Host->Controller   CMD          0x08   0x008  0x2008 LE Set Advertising Data
82    70273.89     Controller->Host   EVT          0x08   0x008  0x0E Command Complete -> LE Set Advertising Data [Success]
83    70275.51     Host->Controller   CMD          0x08   0x00A  0x200A LE Set Advertising Enable
84    70278.70     Controller->Host   EVT          0x08   0x00A  0x0E Command Complete -> LE Set Advertising Enable [Success]
85    72992.90     Controller->Host   EVT          -      -      0x04 Connection Request
86    72995.39     Host->Controller   CMD          0x01   0x009  0x0409 Accept Connection Request
87    72996.74     Controller->Host   EVT          -      -      0x0F Command Status
88    73023.38     Controller->Host   EVT          -      -      0x20 Page Scan Repetition Mode Change
89    73023.75     Controller->Host   EVT          -      -      0x03 Connection Complete Handle=0x0001 Addr=A8:6E:4E:43:F3:B9
90    73027.08     Host->Controller   CMD          0x01   0x00F  0x040F Change Connection Packet Type
91    73027.24     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
92    73028.70     Controller->Host   EVT          -      -      0x0F Command Status
93    73028.85     Host->Controller   CMD          0x02   0x009  0x0809 OGF=0x02, OCF=0x009
94    73030.14     Controller->Host   EVT          0x02   0x009  0x0E Command Complete -> OGF=0x02, OCF=0x009 [Success]
95    73030.31     Host->Controller   CMD          0x02   0x00D  0x080D Exit Sniff Mode
96    73031.70     Controller->Host   EVT          0x02   0x00D  0x0E Command Complete -> Exit Sniff Mode [Success]
97    73032.15     Host->Controller   CMD          0x01   0x01B  0x041B OGF=0x01, OCF=0x01B
98    73033.62     Controller->Host   EVT          -      -      0x0F Command Status
99    73033.75     Host->Controller   CMD          0x01   0x019  0x0419 Remote Name Request
100   73035.15     Controller->Host   EVT          -      -      0x0F Command Status
101   73040.37     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
102   73040.62     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
103   73041.82     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
104   73041.94     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
105   73043.15     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
106   73043.26     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
107   73045.76     Controller->Host   EVT          -      -      0x1B Event_0x1B
108   73051.77     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
109   73069.19     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
110   73069.59     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
111   73071.92     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
112   73073.09     Controller->Host   EVT          -      -      0x07 Event_0x07
113   73073.75     Controller->Host   EVT          -      -      0x1D Event_0x1D
114   73075.20     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
115   73075.31     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
116   73075.41     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
117   73077.68     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
118   73079.17     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
119   73080.29     Controller->Host   EVT          -      -      0x0B Event_0x0B
120   73080.63     Controller->Host   EVT          -      -      0x38 Event_0x38
121   73080.74     Host->Controller   CMD          0x01   0x01C  0x041C OGF=0x01, OCF=0x01C
122   73082.23     Controller->Host   EVT          -      -      0x0F Command Status
123   73082.32     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
124   73083.43     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
125   73084.71     Controller->Host   EVT          -      -      0x23 Event_0x23
126   73086.09     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
127   73087.37     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
128   73088.95     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
129   73103.93     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
130   73106.04     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
131   73106.30     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
132   73106.34     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
133   73108.80     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
134   73110.30     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
135   73115.28     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
136   73115.82     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
137   73120.50     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
138   73122.85     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
139   73124.44     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
140   73153.00     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
141   73158.06     Controller->Host   EVT          -      -      0x17 Event_0x17
142   73158.43     Host->Controller   CMD          0x01   0x00C  0x040C OGF=0x01, OCF=0x00C
143   73159.79     Controller->Host   EVT          0x01   0x00C  0x0E Command Complete -> OGF=0x01, OCF=0x00C [Success]
144   73189.26     Controller->Host   EVT          -      -      0x32 Event_0x32
145   73189.56     Controller->Host   EVT          -      -      0x31 Event_0x31
146   73189.83     Host->Controller   CMD          0x01   0x02B  0x042B OGF=0x01, OCF=0x02B
147   73191.35     Controller->Host   EVT          0x01   0x02B  0x0E Command Complete -> OGF=0x01, OCF=0x02B [Success]
148   73294.40     Controller->Host   EVT          -      -      0x33 Event_0x33
149   73294.79     Host->Controller   CMD          0x01   0x02C  0x042C OGF=0x01, OCF=0x02C
150   73296.16     Controller->Host   EVT          0x01   0x02C  0x0E Command Complete -> OGF=0x01, OCF=0x02C [Success]
151   73595.89     Controller->Host   EVT          -      -      0x36 Event_0x36
152   73607.01     Controller->Host   EVT          -      -      0x18 Event_0x18
153   73613.80     Host->Controller   CMD          0x03   0x07D  0x0C7D Read Local OOB Extended Data
154   73621.03     Controller->Host   EVT          0x03   0x07D  0x0E Command Complete -> Read Local OOB Extended Data [Success]
155   73636.26     Controller->Host   EVT          -      -      0x08 Event_0x08
156   73643.02     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
157   73644.63     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
158   73647.23     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
159   73654.35     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
160   73655.76     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
161   73655.94     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
162   73655.98     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
163   73663.09     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
164   73664.52     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
165   73664.78     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
166   73667.21     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
167   73668.41     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
168   73672.30     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
169   73672.55     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
170   73681.76     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
171   73687.90     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
172   73688.91     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
173   73693.59     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
174   73698.01     Host->Controller   CMD          0x08   0x00A  0x200A LE Set Advertising Enable
175   73702.74     Controller->Host   EVT          0x08   0x00A  0x0E Command Complete -> LE Set Advertising Enable [Success]
176   73705.80     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
177   73707.18     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
178   73709.35     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
179   73709.83     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
180   73709.91     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
181   73714.17     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
182   73715.60     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
183   73716.77     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
184   73755.87     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
185   73763.12     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
186   73766.72     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
187   73772.83     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
188   73777.76     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
189   73790.60     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
190   73807.79     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
191   73807.92     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
192   73812.96     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
193   73815.29     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
194   73815.96     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
195   73817.73     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
196   73847.96     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
197   73849.12     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
198   73851.62     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
199   73852.08     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
200   73852.15     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
201   73861.63     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
202   73864.22     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
203   73865.45     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
204   73871.30     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
205   73878.13     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
206   73882.96     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
207   73901.52     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
208   73928.45     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
209   73944.34     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
210   74010.20     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
211   74016.73     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
212   74028.01     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
213   74042.52     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
214   74048.27     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
215   74060.57     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
216   74070.33     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
217   74076.74     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
218   74091.92     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
219   78380.90     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
220   78412.46     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
221   78412.57     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
222   78437.95     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
223   78439.14     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
224   78469.10     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
225   78471.39     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
226   78491.47     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
227   78501.68     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
228   78554.16     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
229   78555.75     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
230   78560.57     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
231   78585.46     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
232   79466.58     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
233   79470.84     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
234   79496.67     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
235   79501.54     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
236   79505.83     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
237   79531.68     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
238   79534.08     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
239   79672.47     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
240   79691.25     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
241   81480.79     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
242   81515.43     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
243   81523.50     Host->Controller   CMD          0x08   0x00A  0x200A LE Set Advertising Enable
244   81525.34     Controller->Host   EVT          0x08   0x00A  0x0E Command Complete -> LE Set Advertising Enable [Success]
245   81531.54     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
246   81647.72     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
247   81647.97     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
248   81654.85     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
249   81656.40     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
250   81656.82     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
251   81685.38     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
252   81686.54     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
253   81687.81     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
254   81716.84     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
255   85749.03     Controller->Host   EVT          -      -      0x05 Disconnection Complete
256   96045.20     Controller->Host   EVT          -      -      0x04 Connection Request
257   96045.60     Host->Controller   CMD          0x01   0x009  0x0409 Accept Connection Request
258   96048.41     Controller->Host   EVT          -      -      0x0F Command Status
259   96067.92     Controller->Host   EVT          -      -      0x20 Page Scan Repetition Mode Change
260   96068.70     Controller->Host   EVT          -      -      0x03 Connection Complete Handle=0x0001 Addr=A8:6E:4E:43:F3:B9
261   96069.18     Host->Controller   CMD          0x01   0x00F  0x040F Change Connection Packet Type
262   96069.25     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
263   96070.66     Controller->Host   EVT          -      -      0x0F Command Status
264   96070.76     Host->Controller   CMD          0x02   0x009  0x0809 OGF=0x02, OCF=0x009
265   96072.17     Controller->Host   EVT          0x02   0x009  0x0E Command Complete -> OGF=0x02, OCF=0x009 [Success]
266   96072.39     Host->Controller   CMD          0x02   0x00D  0x080D Exit Sniff Mode
267   96073.75     Controller->Host   EVT          0x02   0x00D  0x0E Command Complete -> Exit Sniff Mode [Success]
268   96074.03     Host->Controller   CMD          0x01   0x01B  0x041B OGF=0x01, OCF=0x01B
269   96075.45     Controller->Host   EVT          -      -      0x0F Command Status
270   96075.56     Host->Controller   CMD          0x01   0x019  0x0419 Remote Name Request
271   96076.93     Controller->Host   EVT          -      -      0x0F Command Status
272   96143.88     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
273   96144.01     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
274   96145.32     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
275   96145.43     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
276   96146.67     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
277   96146.76     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
278   96152.28     Controller->Host   EVT          -      -      0x1B Event_0x1B
279   96153.98     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
280   96156.98     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
281   96159.07     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
282   96159.28     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
283   96159.33     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
284   96161.07     Controller->Host   EVT          -      -      0x07 Event_0x07
285   96161.51     Controller->Host   EVT          -      -      0x1D Event_0x1D
286   96161.62     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
287   96161.72     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
288   96162.97     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
289   96164.12     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
290   96165.57     Controller->Host   EVT          -      -      0x0B Event_0x0B
291   96165.95     Controller->Host   EVT          -      -      0x38 Event_0x38
292   96166.05     Host->Controller   CMD          0x01   0x01C  0x041C OGF=0x01, OCF=0x01C
293   96167.47     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
294   96167.52     Controller->Host   EVT          -      -      0x0F Command Status
295   96167.58     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
296   96170.52     Controller->Host   EVT          -      -      0x23 Event_0x23
297   96170.78     Controller->Host   EVT          -      -      0x32 Event_0x32
298   96170.81     Controller->Host   EVT          -      -      0x31 Event_0x31
299   96170.94     Host->Controller   CMD          0x01   0x02B  0x042B OGF=0x01, OCF=0x02B
300   96172.36     Controller->Host   EVT          0x01   0x02B  0x0E Command Complete -> OGF=0x01, OCF=0x02B [Success]
301   96252.99     Controller->Host   EVT          -      -      0x33 Event_0x33
302   96259.57     Host->Controller   CMD          0x01   0x02C  0x042C OGF=0x01, OCF=0x02C
303   96262.29     Controller->Host   EVT          0x01   0x02C  0x0E Command Complete -> OGF=0x01, OCF=0x02C [Success]
304   96503.21     Controller->Host   EVT          -      -      0x36 Event_0x36
305   96514.02     Controller->Host   EVT          -      -      0x18 Event_0x18
306   96516.84     Host->Controller   CMD          0x03   0x07D  0x0C7D Read Local OOB Extended Data
307   96519.47     Controller->Host   EVT          0x03   0x07D  0x0E Command Complete -> Read Local OOB Extended Data [Success]
308   96556.49     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
309   96557.00     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
310   96558.26     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
311   96561.98     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
312   96563.16     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
313   96563.29     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
314   96563.32     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
315   96566.41     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
316   96567.82     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
317   96571.34     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
318   96571.71     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
319   96576.97     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
320   96578.87     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
321   96581.40     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
322   96596.98     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
323   96598.97     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
324   96599.53     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
325   96600.81     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
326   96617.00     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
327   96618.19     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
328   96618.32     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
329   96618.35     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
330   96621.67     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
331   96623.23     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
332   96625.11     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
333   96625.54     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
334   96630.25     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
335   96633.19     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
336   96633.50     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
337   96650.99     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
338   96653.98     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
339   96654.36     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
340   96660.06     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
341   96662.61     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
342   96662.93     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
343   96667.81     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
344   96671.97     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
345   96672.32     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
346   96689.01     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
347   96693.76     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
348   96694.08     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
349   96727.78     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
350   96730.22     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
351   96730.47     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
352   96735.35     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
353   96737.53     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
354   96737.79     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
355   96752.00     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
356   96756.69     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
357   96757.03     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
358   96774.06     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
359   96778.92     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
360   96779.26     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
361   96784.14     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
362   96791.37     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
363   96791.61     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
364   96796.90     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
365   96798.97     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
366   96800.36     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
367   96817.01     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
368   96872.69     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
369   96873.30     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
370   96874.63     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
371   96890.32     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
372   96892.15     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
373   96893.37     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
374   96893.55     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
375   96896.45     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
376   96897.96     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
377   96902.06     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
378   96902.53     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
379   96919.11     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
380   96920.30     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
381   96921.71     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
382   96937.81     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
383   96952.99     Controller->Host   EVT          -      -      0x08 Event_0x08
384   96957.66     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
385   96958.06     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
386   96959.78     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
387   96963.54     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
388   96964.74     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
389   96964.93     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
390   96964.97     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
391   96970.20     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
392   96971.59     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
393   96971.64     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
394   96971.74     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
395   96976.93     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
396   96978.16     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
397   96978.33     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
398   96995.30     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
399   96996.47     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
400   97000.54     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
401   97000.63     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
402   97000.68     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
403   97014.01     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
404   97015.29     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
405   97016.52     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
406   97017.83     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
407   97017.92     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
408   97017.95     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
409   97019.29     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
410   97041.52     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
411   97041.68     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
412   97042.86     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
413   97043.03     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
414   97044.19     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
415   97045.40     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
416   97050.65     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
417   97051.21     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
418   97067.79     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
419   97071.34     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0041,Dynamic_CID_0x0041)
420   97073.05     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
421   97077.00     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
422   97080.15     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
423   97123.05     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
424   97125.48     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
425   97130.70     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
426   97131.57     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
427   97132.18     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
428   97147.82     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
429   97151.42     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
430   97152.03     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
431   97167.10     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
432   97173.09     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
433   97175.11     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
434   97175.41     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
435   97182.83     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
436   97185.21     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
437   97187.22     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
438   97187.75     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
439   97204.03     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
440   97206.35     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
441   97206.76     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
442   97211.97     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
443   97213.84     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
444   97215.38     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
445   97216.54     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
446   97232.77     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
447   97240.36     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
448   97244.95     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
449   97257.76     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
450   97259.03     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
451   97259.89     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
452   97277.00     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
453   97279.28     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
454   97279.91     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
455   97282.12     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
456   97295.90     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
457   97297.09     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
458   97297.15     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
459   97297.72     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
460   97300.47     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
461   97302.79     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
462   97304.14     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
463   97304.26     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
464   97304.32     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
465   97305.90     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
466   97306.57     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
467   97307.86     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
468   97307.91     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
469   97309.02     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
470   97311.82     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
471   97312.18     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
472   97336.57     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
473   97337.34     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
474   97338.60     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
475   97341.26     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
476   97350.09     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0041,Dynamic_CID_0x0041)
477   97351.87     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
478   97351.97     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
479   97351.99     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
480   97352.47     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
481   97357.07     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
482   97358.22     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
483   97358.25     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0001,L2CAP_Signaling)
484   97359.73     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
485   97363.60     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
486   97364.00     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
487   97364.44     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
488   97364.51     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
489   97368.99     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
490   97370.29     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
491   97371.41     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
492   97372.23     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
493   97388.87     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
494   97390.55     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
495   97390.65     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
496   97405.11     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
497   97406.29     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
498   97406.40     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
499   97406.44     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
500   97407.76     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
501   97412.00     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
502   97413.18     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
503   97413.88     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
504   97415.29     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
505   99813.94     Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
506   99824.04     Controller->Host   EVT          -      -      0x13 Number of Completed Packets
507   99832.60     Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
508   104150.38    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
509   104172.96    Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
510   104182.93    Controller->Host   EVT          -      -      0x13 Number of Completed Packets
511   104200.01    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
512   104203.36    Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
513   104230.29    Controller->Host   EVT          -      -      0x13 Number of Completed Packets
514   104241.34    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
515   111258.43    Controller->Host   EVT          -      -      0x14 Event_0x14
516   164172.18    Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
517   164293.36    Controller->Host   EVT          -      -      0x13 Number of Completed Packets
518   164790.49    Controller->Host   EVT          -      -      0x14 Event_0x14
519   164793.13    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
520   164998.22    Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
521   165005.84    Controller->Host   EVT          -      -      0x13 Number of Completed Packets
522   165016.89    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
523   165230.83    Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
524   165254.72    Controller->Host   EVT          -      -      0x13 Number of Completed Packets
525   165281.88    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
526   165493.04    Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
527   165518.77    Controller->Host   EVT          -      -      0x13 Number of Completed Packets
528   165529.35    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
529   165532.39    Host->Controller   SCO_TX       0x00   0x102  0x0102 OGF=0x00, OCF=0x102
530   165559.66    Controller->Host   EVT          -      -      0x13 Number of Completed Packets
531   165588.27    Host->Controller   ACL_TX       -      -      Handle=0x0001 L2CAP(0x0040,Dynamic_CID_0x0040)
532   172582.80    Controller->Host   EVT          -      -      0x14 Event_0x14
```

## 📝 分析总结

1. **连接管理**: 2 个连接建立，1 个断开

2. **数据传输**: 125 个 ACL 数据包，句柄 0x0001

3. **错误状态**: 未发现 HCI 层错误

---

**架构**: BTSnoop → HCI(命令/事件/ACL) → L2CAP(信令/ATT) → 可扩展 SDP 等
