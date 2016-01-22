data = csvread('mwl.csv');
palette = load_bwrc_colors();

% Lets take a subset
mwl_true = boolean(data(:, 4));

figure();
	subplot(2, 1, 1);
	hold on;
	plot(data(mwl_true, 1), data(mwl_true, 2), 'o', 'markerfacecolor', palette.orange, 'color', palette.dblue);
	plot(data(:, 1), data(:, 2), '-o', 'markerfacecolor', 'w', 'color', palette.dblue);
	plot(data(mwl_true, 1), data(mwl_true, 2), 'o', 'markerfacecolor', palette.orange, 'color', palette.dblue);
	hold off;
	box on;
	set(gca, 'xlim', [data(1, 1)- 1, data(end, 1) + 1]);
	legend({'High mental workload'});
	xlabel('Time [seconds]');
	ylabel('Brainbeat [arbitrary units]');

	subplot(2, 1, 2);
	hold on;
	plot(data(:, 1), data(:, 3), '-o', 'markerfacecolor', 'w', 'color', palette.dblue);
	plot(data(mwl_true, 1), data(mwl_true, 3), 'o', 'markerfacecolor', palette.orange, 'color', palette.dblue);
	hold off;
	box on;
	set(gca, 'xlim', [data(1, 1)- 1, data(end, 1) + 1]);
	xlabel('Time [seconds]');
	ylabel('Average heart rate [bmp]');
