from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    mm1_results = None
    error = None
    
    if request.method == 'POST':
        try:
            arrival_time = float(request.form['arrival_time'])
            service_time = float(request.form['service_time'])

            if arrival_time <= 0 or service_time <= 0:
                error = "Waktu harus positif."
            else:
                # Basic Rate
                lam = 1 / arrival_time
                mu = 1 / service_time

                # --- 1. HITUNG M/M/2 (TUGAS UTAMA) ---
                # Cek kestabilan: mu - (lambda/2) > 0
                denom_mm2 = mu - (lam / 2)
                
                if denom_mm2 <= 0:
                    error = "Sistem M/M/2 Overload (Pelanggan datang terlalu cepat untuk 2 server)."
                else:
                    rho_2 = lam / (2 * mu)
                    w_2 = 1 / denom_mm2
                    # Wq Rumus PDF: lambda^2 / (2mu * denom)
                    wq_2 = (lam**2) / ((2 * mu) * denom_mm2)
                    
                    l_2 = lam * w_2   # Little's Law
                    lq_2 = lam * wq_2 # Little's Law

                    results = {
                        'input_arrival': arrival_time,
                        'input_service': service_time,
                        'rho': round(rho_2, 4),
                        'rho_percent': round(rho_2 * 100, 2),
                        'w': round(w_2, 4),
                        'wq': round(wq_2, 4),
                        'l': round(l_2, 4),
                        'lq': round(lq_2, 4),
                        'lam': round(lam, 4),
                        'mu': round(mu, 4),
                        'calc_denom': round(denom_mm2, 4),
                        'calc_2mu': round(2*mu, 4),
                        'lam_sq': round(lam**2, 5)
                    }

                    # --- 2. HITUNG M/M/1 (PERBANDINGAN) ---
                    # Rumus: W = 1 / (mu - lambda)
                    # Cek kestabilan single server
                    denom_mm1 = mu - lam
                    
                    if denom_mm1 > 0:
                        rho_1 = lam / mu
                        w_1 = 1 / denom_mm1
                        wq_1 = rho_1 * w_1
                        l_1 = lam * w_1
                        lq_1 = lam * wq_1
                        
                        mm1_results = {
                            'rho': round(rho_1, 4),
                            'rho_percent': round(rho_1 * 100, 2),
                            'w': round(w_1, 4),
                            'wq': round(wq_1, 4),
                            'l': round(l_1, 4),
                            'lq': round(lq_1, 4),
                            'status': 'Stable'
                        }
                    else:
                        mm1_results = {
                            'status': 'Unstable',
                            'msg': 'Tidak Stabil (Antrian Tak Terhingga)'
                        }

        except ValueError:
            error = "Input tidak valid."

    return render_template('index.html', results=results, mm1_results=mm1_results, error=error)

if __name__ == '__main__':
    app.run(debug=True)