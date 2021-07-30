<?php
$packet_count = 4;
$max_int = pow(2, 30);
$jitter = $max_int * 0.1;

$output_files = 1;
for ($f = 0; $f < $output_files; $f++) {
    $file_path_dat = "data/test_data_$f.dat";
    $file_path_txt = "data/test_data_$f.txt";
    unlink($file_path_dat);
    unlink($file_path_txt);
    $dataset = fopen($file_path_dat, "wb");
    $dataset_txt = fopen($file_path_txt, "w");
    for ($i = 0; $i < $packet_count; $i++) {
        $radiance = rand(0, 65536);
        $vibration_factor = 1 / rand($max_int - $jitter, $max_int + $jitter);
        echo $vibration_factor . "\n";
        fwrite($dataset_txt, "45, \"2.4\", 1, $radiance, $vibration_factor\n");
        $payload = pack("Ca4cLf", 45, "2.4\0", 1, $radiance, $vibration_factor);  # https://www.php.net/manual/en/function.pack.php
        fwrite($dataset, $payload);
    }
    fclose($dataset);
    fclose($dataset_txt);
}



