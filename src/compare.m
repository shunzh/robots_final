#! /usr/bin/octave -qf

args = dlmread("compare.in");
x = 30 : 120;
y = args(1) * (x .^ 2) + args(2) * x + args(3);
plot (x, y, "r");
hold on;

d = dlmread("obs.data");
plot (d(:, 2), d(:, 1));

pause;
