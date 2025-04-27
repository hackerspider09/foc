% initlization
N = 10^6; 
Eb_No_dB = -3:10; 
Eb_No = 10.^(Eb_No_dB / 10);


% generate Random Bits 
ip = rand(1, N) > 0.5;

% BPSK modulation
s = 2 * ip - 1; 

% arrays to store BER for each Eb/No
nErr_AWGN = zeros(1, length(Eb_No_dB));
nErr_Rayleigh = zeros(1, length(Eb_No_dB));

% noise
n = 1/sqrt(2) * (randn(1, N) + 1j * randn(1, N));

% simulation for each Eb/No value
for ii = 1:length(Eb_No_dB)
    % AWGN
    y_AWGN = s + 10^(-Eb_No_dB(ii)/20) * n;

    % h rayleigh
    h_Rayleigh = 1/sqrt(2) * (randn(1, N) + 1j * randn(1, N));
    
     % signal with fading
    y_Rayleigh = h_Rayleigh .* s + 10^(-Eb_No_dB(ii)/20) * n;

    % equalization
    y_equalized = y_Rayleigh ./ h_Rayleigh;

    % decoding received signal back to bits
    ipHat_AWGN = real(y_AWGN) > 0;
    ipHat_Rayleigh = real(y_equalized) > 0;

    % count errors
    nErr_AWGN(ii) = sum(ip ~= ipHat_AWGN);
    nErr_Rayleigh(ii) = sum(ip ~= ipHat_Rayleigh);
end

% simulated BER
simBer_AWGN = nErr_AWGN / N; 
simBer_Rayleigh = nErr_Rayleigh / N;

% theoretical BER
theoryBer_AWGN = 0.5 * erfc(sqrt(Eb_No));
theoryBer_Rayleigh = 0.5 * (1 - sqrt(Eb_No ./ (1 + Eb_No)));

% plot
figure;
semilogy(Eb_No_dB, theoryBer_AWGN, 'b.-', 'LineWidth', 1.5); hold on;
semilogy(Eb_No_dB, simBer_AWGN, 'mx-', 'LineWidth', 1.5);
semilogy(Eb_No_dB, theoryBer_Rayleigh, 'r.-', 'LineWidth', 1.5);
semilogy(Eb_No_dB, simBer_Rayleigh, 'gx-', 'LineWidth', 1.5);
grid on;
legend('Theory (AWGN)', 'Simulation (AWGN)', 'Theory (Rayleigh)', 'Simulation (Rayleigh)');
xlabel('Eb/No (dB)');
ylabel('Bit Error Rate (BER)');
title('Bit Error Rate (BER) for BPSK in AWGN and Rayleigh Fading');
