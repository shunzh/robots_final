#! /usr/bin/octave -qf

e = dlmread("err.out");
plot(e(:, 1))
hold on;
plot(e(:, 2), "r")
pause;
