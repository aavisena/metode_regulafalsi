<?php
function f($x) {
    return pow($x, 3) - 4*$x - 9;
}

$result = [];
if (isset($_POST['hitung'])) {
    $a = floatval($_POST['a']);
    $b = floatval($_POST['b']);
    $tol = floatval($_POST['toleransi']);
    $maxIter = intval($_POST['iterasi']);

    if (f($a) * f($b) >= 0) {
        $error = "Nilai f(a) dan f(b) harus berlainan tanda!";
    } else {
        for ($i = 1; $i <= $maxIter; $i++) {
            $fa = f($a);
            $fb = f($b);
            $xr = ($a * $fb - $b * $fa) / ($fb - $fa);
            $fxr = f($xr);

            $result[] = [$i, $a, $b, $xr, $fxr];

            if (abs($fxr) < $tol) break;
            if ($fa * $fxr < 0) $b = $xr;
            else $a = $xr;
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
<title>Regula Falsi Web</title>
<style>
body{font-family:Arial;background:#f4f4f4}
.container{width:700px;margin:auto;background:#fff;padding:20px}
table{width:100%;border-collapse:collapse;margin-top:20px}
th,td{border:1px solid #ccc;padding:8px;text-align:center}
th{background:#eee}
</style>
</head>
<body>
<div class="container">
<h2>Metode Regula Falsi</h2>
<form method="POST">
<input type="number" step="any" name="a" placeholder="Batas bawah a" required>
<input type="number" step="any" name="b" placeholder="Batas atas b" required>
<input type="number" step="any" name="toleransi" value="0.0001" required>
<input type="number" name="iterasi" value="20" required>
<button name="hitung">Hitung</button>
</form>

<?php if (!empty($result)) { ?>
<table>
<tr><th>i</th><th>a</th><th>b</th><th>xr</th><th>f(xr)</th></tr>
<?php foreach ($result as $r) { ?>
<tr>
<td><?= $r[0] ?></td>
<td><?= round($r[1],6) ?></td>
<td><?= round($r[2],6) ?></td>
<td><?= round($r[3],6) ?></td>
<td><?= round($r[4],6) ?></td>
</tr>
<?php } ?>
</table>
<p><b>Akar ≈ <?= round(end($result)[3],6) ?></b></p>
<?php } ?>
</div>
</body>
</html>
