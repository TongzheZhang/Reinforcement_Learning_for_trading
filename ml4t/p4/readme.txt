#created by Tongzhe Zhang
You can run my code p4.py to create the out-sample backtest of ML4T-240.
If you want to generate other charts, you need to modify the p4.py.
If you want to get (price,Y,predY) charts, you can add comments on lines 148(position4),cancel the comments on lines 149,cancel comments on lines 193,195(position6),cancel comments on lines 202,203,204,204,add comments on last line(position2)
If you want to get (price,enter,exit) charts, you can cancel comments on lines 202,203,204,204,add comments on last line(position2),change the plotif from false to true(lines 207,position3)
if you want to change symbols, you just need to replace all ML4T-240 to IBM
if you want to change out_example to in-sample, just to change the date on position3 and position5