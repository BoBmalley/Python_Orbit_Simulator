a = 905
b = 1
hul = 0.00
rangelist = [0,
             200,
             250,
             350,
             450,
             550,
             650,
             750,
             850,
             950,
             1000,
             1100,
             1200,
             1250,
             1350,
             1400,
             1500,
             1550,
             1600,
             1700,
             1750,
             1800,
             1900,
             1950,
             2000]
yaoyle = [-4, 6]

for i in range(0, len(rangelist)):
    line = "text {{ text:t = \" {} s\"; pos:p2 = -17.6, 12.0; size:r = 0.4; align:i = 2; radialAngle:r = {}; highlight:b = yes; radialCenter:p2 = 1000000, 0; radialMoveSpeed:r = 997; moveRadial:b = yes; thousandth:b = yes; }}"
    line = line.format(round((b * rangelist[i]) / a, 2), hul + (i * 0.04))
    print(line)
