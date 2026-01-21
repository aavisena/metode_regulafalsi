<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Aplikasi Regula Falsi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background:#f4f6f8; padding:16px; }
        .box { background:#fff; padding:16px; border-radius:8px; max-width:720px; margin:auto; box-shadow:0 0 10px rgba(0,0,0,.1); }
        h2 { margin-top:0; }
        label { font-weight:bold; }
        input, button { width:100%; padding:10px; margin:8px 0 14px; }
        button { background:#2563eb; color:#fff; border:none; border-radius:6px; }
        table { width:100%; border-collapse:collapse; margin-top:14px; }
        th, td { border:1px solid #000; padding:6px; text-align:center; }
        .note { font-size:12px; color:#555; }
    </style>
</head>
<body>
<div class="box">
    <h2>Aplikasi Web Metode Regula Falsi</h2>

    <label>Persamaan f(x)</label>
    <input id="fx" placeholder="Contoh: x*x*x - x - 2" value="x*x*x - x - 2">

    <label>Nilai a</label>
    <input id="a" type="number" step="any" value="1">

    <label>Nilai b</label>
    <input id="b" type="number" step="any" value="2">

    <label>Toleransi Error</label>
    <input id="err" type="number" step="any" value="0.0001">

    <button onclick="hitung()">Hitung</button>

    <div id="out"></div>
    <p class="note">Catatan: gunakan operator *, /, +, - dan x sebagai variabel.</p>
</div>

<script>
function hitung(){
    const fx = document.getElementById('fx').value;
    let a = parseFloat(document.getElementById('a').value);
    let b = parseFloat(document.getElementById('b').value);
    const err = parseFloat(document.getElementById('err').value);

    const f = new Function('x', 'return ' + fx);

    if (isNaN(a) || isNaN(b) || isNaN(err)) {
        alert('Input tidak valid');
        return;
    }
    if (f(a)*f(b) >= 0){
        alert('f(a) dan f(b) harus berlainan tanda');
        return;
    }

    let xr = 0, iter = 0;
    let table = `<table><tr><th>Iterasi</th><th>a</th><th>b</th><th>x_r</th><th>f(x_r)</th></tr>`;

    do{
        xr = (a*f(b) - b*f(a)) / (f(b) - f(a));
        table += `<tr><td>${iter+1}</td><td>${a.toFixed(6)}</td><td>${b.toFixed(6)}</td><td>${xr.toFixed(6)}</td><td>${f(xr).toFixed(6)}</td></tr>`;
        if (f(a)*f(xr) < 0) b = xr; else a = xr;
        iter++;
        if (iter > 100) break;
    } while (Math.abs(f(xr)) > err);

    table += `</table>`;
    document.getElementById('out').innerHTML = `<h3>Hasil</h3><p>Akar ≈ <b>${xr.toFixed(6)}</b><br>Iterasi: ${iter}</p>` + table;
}
</script>
</body>
</html>
