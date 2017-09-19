
<html>
<body>
<?php
$url = "https://www.cleverbot.com/getreply";
$key = "6c3f005ec8f79dd543c7cca772a75fa9";
$input = rawurlencode ("Hello World!");
$current = file_get_contents("$url?input=$input&key=$key");
$obj = json_decode($current);
print $obj->{'output'};
?>
</body>
</html>
