# soham
import numpy as np

def generate_walsh_matrix(n):
    if n == 1:
        return np.array([[1]])
    smaller = generate_walsh_matrix(n //2)
    top = np.hstack((smaller, smaller))
    bottom = np.hstack((smaller, -smaller))
    return np.vstack((top, bottom))

def cdma_simulation(num_users=8, intended_bit=1, noise_floor=1e-6):
    walsh_matrix = generate_walsh_matrix(num_users)
    print("Walsh Code Matrix:")
    print(walsh_matrix)
    print("\n" + "="*50 + "\n")

    intended_index = 5
    print(f"Intended User: {intended_index}, Transmitting bit: {intended_bit}\n")

    transmitted_signal = intended_bit * walsh_matrix[intended_index]
    noise = np.random.normal(0, 0.5, num_users)
    noisy_signal = transmitted_signal + noise

    print("Transmitted Signal (before noise):")
    print(transmitted_signal)
    print("\nNoise Added:")
    print(noise)
    print("\nReceived Signal (with noise):")
    print(noisy_signal)
    print("\n" + "="*50 + "\n")

    results = []
    for i in range(num_users):
        correlation = np.dot(noisy_signal, walsh_matrix[i]) / num_users
        signal_power = 1.0 if i == intended_index else 0.0
        if i == intended_index:
            noise_power = np.var(noise)
        else:
            interference = np.dot(walsh_matrix[intended_index], walsh_matrix[i]) / num_users
            noise_power = interference**2 + np.var(noise)
        if noise_power > 0:
            snr = signal_power / noise_power
            if snr > 0:
                snr_db = 10 * np.log10(snr)
            else:
                snr_db = float('-inf')
        else:
            snr = float('inf')
            snr_db = float('inf')
        results.append({
            'user': i + 1,
            'type': 'Intended' if i == intended_index else 'Unintended',
            'correlation': correlation,
            'signal_power': signal_power,
            'noise_power': noise_power,
            'snr_db': snr_db
        })

    print("User\tType\tCorrelation\tSignal Power\tNoise Power\tSNR (dB)")
    print("-"*80)
    for res in results:
        print(f"{res['user']}\t{res['type']:12}\t{res['correlation']:+.4f}\t"
              f"{res['signal_power']:.6f}\t{res['noise_power']:.6f}\t"
              f"{res['snr_db']:+.2f}")

    intended = results[intended_index]
    unintended = [r for r in results if r['type'] == 'Unintended']
    avg_unintended_snr = np.mean([r['snr_db'] for r in unintended])

    print("\nSUMMARY RESULTS:")
    print(f"Intended User {intended['user']}: ")
    print(f"Correlation: {intended['correlation']:+.4f}")
    print(f"SNR: {intended['snr_db']:.2f} dB")
    print(f"Signal Power: {intended['signal_power']:.6f}")
    print(f"Noise Power: {intended['noise_power']:.6f}")
    print("\nAverage Unintended User:")
    print(f"Avg Correlation: {np.mean([r['correlation'] for r in unintended]):.6f}")
    print(f"Avg SNR: {avg_unintended_snr:+.2f} dB")
    print(f"Avg Signal Power: {np.mean([r['signal_power'] for r in unintended]):.6f}")
    print(f"Avg Noise Power: {np.mean([r['noise_power'] for r in unintended]):.6f}")

if __name__ == '__main__':
    cdma_simulation(num_users=8, intended_bit=1, noise_floor=1e-6)