#! /usr/bin/octave -qf

args = dlmread("action.in");
disp(args);
x = -1 : .01 : 1;
y = args(1) + args(2) * x + args(3) * (x .^ 2) + args(3) * (x .^ 3);
plot (x, y, "r");
hold on;

pause;
