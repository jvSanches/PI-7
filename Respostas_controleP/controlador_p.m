L ='ref';
data = no_mecanismo; %ndata; %boost_completo;
data_start = data(1,1);
[len, wid] = size(data);
data_end = data(len,1);

for Kp = data_start:1:data_end
    delta_pos = data(Kp - (data_start-1), :);
    samples = length(delta_pos)-1;

    t = 0.005: 0.005 :(0.005 * samples);
    pos = zeros(samples,0);

    pos(1) = delta_pos(2);
    for i = 2:samples
        pos(i) = pos(i-1) + delta_pos(i+1);
    end

    plot(t,pos,'LineWidth',1);
    ylim([0 200]);
    refline(0,100);
    %text(0.7+((Kp-data_start)/50), pos(100)+15, "Kp = " + string(Kp));
    L = [L,string(Kp)];
    legend(L);
    hold on;
end
title("Amplitude: 100 ticks");
%suptitle("Resposta ao degrau ");
suptitle("Resposta ao degrau");
xlabel("Tempo [s]");
ylabel("Posição [ticks]");