d = dlmread("out_strong.lgdat");
d(:, 1) /= 100;
plot(d);
xlabel("Number of Frames");
ylabel("Measurement");
legend("Beacon Height", "w_a", "w_s");
print("out_strong.png", "-S700,550");
