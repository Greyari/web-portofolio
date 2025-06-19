<?php
$host = 'centerbeam.proxy.rlwy.net';
$port = 49539;
$dbname = 'railway';
$username = 'root';
$password = 'orMziNHAmFwnaLnMCGUcfhinHedEYGBR';

try {
    $pdo = new PDO("mysql:host=$host;port=$port;dbname=$dbname", $username, $password);
    echo "✅ Koneksi berhasil ke Railway MySQL!";
} catch (PDOException $e) {
    echo "❌ Gagal konek: " . $e->getMessage();
}
