<?php
	$output = shell_exec('python temp.py');
	echo "<pre>$output</pre>";
	header("Refresh:3");
?>
