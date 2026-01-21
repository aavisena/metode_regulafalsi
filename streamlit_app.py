<?php
// ===============================
// METODE REGULA FALSI
// ===============================

// Fungsi nonlinear
function f($x) {
    return pow($x, 3) - 4*$x - 9; // f(x) = x^3 - 4x - 9
}

$hasil = [];

if (isset($_POST['hitung'])) {
    $a = floatval($_POST['a']);
    $b = floatval($_POST['b']);
    $toleransi = floatval($_POST['toleransi']);
    $maksIterasi = intval($_POST['iterasi']);

    if (f($a) * f($b) >= 0) {
        $error = "f(a) dan f(b) harus memiliki tanda berbeda!";
    } else {
        for ($i = 1; $i <= $maksIterasi; $i++) {
            $fa = f($a);
            $fb = f($b);

            $xr = ($a * $fb - $b * $fa) / ($fb - $fa);
            $fxr = f($xr);

            $hasil[] = [
                'iterasi' => $i,
                'a' => $a,
                'b' => $b,
                'xr' => $xr,
                'fxr' => $fxr
            ];

            if (abs($fxr) < $toleransi) {
                break;
            }

            if ($fa * $fxr < 0) {
                $b = $xr;
            } else {
                $a = $xr;
            }
        }
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Metode Regula Falsi</title>
    <style>
        body { font-family: Arial; background: #f2f2f2; }
        .container { width: 750px; margin: auto; background: #fff; padding: 20px; }
        input, button { padding: 8px; width: 100%; margin: 5px 0; }
        button { background: #007bff; color: #fff; border: none; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background: #eee; }
        .error { color: red; margin-top: 10px; }
    </style>
</head>
<body>

<div class="container">
    <h2>Aplikasi Web Metode Regula Falsi</h2>
    <p><b>Fungsi:</b> f(x) = x³ − 4x − 9</p>

    <form method="POST">
        <label>Batas bawah (a)</label>
        <input type="number" step="any" name="a" required>

        <label>Batas atas (b)</label>
        <input type="number" step="any" name="b" required>

        <label>Toleransi error</label>
        <input type="number" step="any" name="toleransi" value="0.0001" required>

        <label>Maksimum iterasi</label>
        <input type="number" name="iterasi" value="20" required>

        <button type="submit" name="hitung">Hitung</button>
    </form>

    <?php if (isset($error)) : ?>
        <div class="error"><?= $error ?></div>
    <?php endif; ?>

    <?php if (!empty($hasil)) : ?>
        <table>
            <tr>
                <th>Iterasi</th>
                <th>a</th>
                <th>b</th>
                <th>xr</th>
                <th>f(xr)</th>
            </tr>
            <?php foreach ($hasil as $h) : ?>
            <tr>
                <td><?= $h['iterasi'] ?></td>
                <td><?= round($h['a'], 6) ?></td>
                <td><?= round($h['b'], 6) ?></td>
                <td><?= round($h['xr'], 6) ?></td>
                <td><?= round($h['fxr'], 6) ?></td>
            </tr>
            <?php endforeach; ?>
        </table>

        <p><b>Akar hampiran ≈ <?= round(end($hasil)['xr'], 6) ?></b></p>
    <?php endif; ?>
</div>

</body>
</html>
