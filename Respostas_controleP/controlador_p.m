L ='ref';
data = no_boost_data;
data_start = data(1,1);
[len, wid] = size(data);
data_end = data(len,1);

for Kp = data_start:1:data_end
    delta_pos = data(Kp - (data_start-1), :);
    samples = length(delta_pos)-1;

    t = 0.01: 0.01:(0.01 * samples);
    pos = zeros(samples,0);

    pos(1) = delta_pos(2);
    for i = 2:samples
        pos(i) = pos(i-1) + delta_pos(i+1);
    end

    plot(t,pos,'LineWidth',1);
    ylim([0 1200]);
    refline(0,1000);
    text(0.7+((Kp-data_start)/50), pos(100)+15, "Kp = " + string(Kp));
    L = [L,string(Kp)];
    legend(L);
    hold on;
end
title("Amplitude: 1000 ticks  - Correção de PWM");
%suptitle("Resposta ao degrau ");
suptitle("Resposta ao degrau para ganhos variados");
xlabel("Tempo [s]");
ylabel("Posição [ticks]");