\ Model spp problem
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  a1,b2 + a2,b3 + a2,c3 + a4,c5 + b5,f6 + c6,f7 + c7,g8
Subject To
 start_flow: a1,b2 + a1,a2 = 1
 end_flow: c7,g8 = 1
 flow_conservation: = 0
 flow_conservation: a1,b2 - b2,b3 = 0
 flow_conservation: - a2,b3 - a2,c3 + a1,a2 - a2,a4 = 0
 flow_conservation: a2,b3 + b2,b3 - b3,b5 = 0
 flow_conservation: a2,c3 - c3,c5 = 0
 flow_conservation: - a4,c5 + a2,a4 = 0
 flow_conservation: a4,c5 + c3,c5 - c5,c6 = 0
 flow_conservation: - b5,f6 + b3,b5 = 0
 flow_conservation: b5,f6 - f6,f7 = 0
 flow_conservation: - c6,f7 + c5,c6 - c6,c7 = 0
 flow_conservation: c6,f7 + f6,f7 = 0
 flow_conservation: - c7,g8 + c6,c7 = 0
 flow_conservation: = 0
Bounds
Binaries
 a1,b2 a2,b3 a2,c3 a4,c5 b5,f6 c6,f7 c7,g8 a1,a2 a2,a4 b2,b3 b3,b5 c3,c5
 c5,c6 c6,c7 f6,f7
End
