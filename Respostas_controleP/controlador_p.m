L ='ref';
data = boost_data;
data_start = boost_data(1,1);
[len, wid] = size(data);
data_end = boost_data(len,1);

for Kp = data_start:data_end
    delta_pos = data(Kp - (data_start-1), :);
    samples = length(delta_pos)-1;

    t = 0.01: 0.01:(0.01 * samples);
    pos = zeros(samples,0);

    pos(1) = delta_pos(2);
    for i = 2:samples
        pos(i) = pos(i-1) + delta_pos(i+1);
    end

    plot(t,pos);
    ylim([0 1200]);
    refline(0,1000);
    L = [L,string(Kp)];
    legend(L);
    hold on;
end
title("PWM boost  -  Amplitude: 1000 ticks");
suptitle("Resposta ao degrau para ganhos variados");