#! /usr/bin/octave -qf

args = dlmread("sensor.in");
disp(args);
x = 60 : .01 : 140;
y = args(1) + args(2) * x + args(3) * (x .^ 2) + args(3) * (x .^ 3);
plot (x, y, "r");
hold on;

pause;
