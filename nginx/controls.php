<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
		<script type="text/javascript">
			$(document).ready(function(){
				$('#clickON').click(function(){
					var a = new XMLHttpRequest();
					a.open("GET","pinon.php");
					a.onreadystatechange=function(){
						if(a.readyState==4) {
							if(a.status == 200){
							}
							else alert("HTTP ERROR");
						}
					}
					a.send();
				});
				$('#clickOFF').click(function(){
                                        var a = new XMLHttpRequest();
                                        a.open("GET","pinoff.php");
                                        a.onreadystatechange=function(){
                                                if(a.readyState==4) {
                                                        if(a.status == 200){
                                                        }
                                                        else alert("HTTP ERROR");
                                                }
                                        }
                                        a.send();
                                });

			});
		</script>
		<title>Pi Controller</title>
	</head>
	<body>
		<button type="button" id="clickON">ON</button><br>
		<button type="button" id="clickOFF">OFF</button><br>
	</body>
</html>
