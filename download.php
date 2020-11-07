<?php
$filename = "urls.txt";
$save_folder = "./saved/";
$sessionid_cookie = "insert here your session id";

// todo: rewrite this script in python

$array = file($filename, FILE_IGNORE_NEW_LINES);
$options = array('http' => array('method'=>"GET", 'header'=>"Accept-language: en\r\n" . "Cookie: sessionid=$sessionid_cookie\r\n" . "User-Agent: Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10\r\n"));

function get_http_response_code($url) {
	$headers = get_headers($url);
	return substr($headers[0], 9, 3);
}

foreach($array as $key => $url) {
	$context = stream_context_create($options);
	$file_name = $save_folder . basename(parse_url($url, PHP_URL_PATH));
	$content = @file_get_contents($url, false, $context);
	if($content == false) {
		echo "$key : an error downoading the following link: $url<br />note: search for this value or go to line $key+1 !!";
		echo file_get_contents($url, false, $context);
		die();
	} else {
		echo "$key : successfully downloaded <br />";
		file_put_contents($file_name, $content);
	}
	sleep(2);
	flush();
}
?>
