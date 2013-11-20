#! /usr/bin/octave -qf

l = dlmread("log.out");
plot(l(:, 1))
hold on;
plot(l(:, 2), "r")
plot(l(:, 3), "g")
pause;
