d = dlmread("out_obs.para");
obs = d(:, 4:7);
obs_a = obs(1:2:end, :);
obs_s = obs(2:2:end, :);

for i = 1:size(obs_a, 1)
	dis_a(i) = norm(obs_a(i, :) - obs_a(end, :));
endfor

for i = 1:size(obs_s, 1)
	dis_s(i) = norm(obs_s(i, :) - obs_s(end, :));
endfor

save "out_obs_a.mat" dis_a
save "out_obs_s.mat" dis_s
