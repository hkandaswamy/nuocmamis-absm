<?php
$hostname = "prototype-avery.c6j7jqlt2fgj.us-east-2.rds.amazonaws.com";
$database = "test";
$username = "admin";
$password = "0sQO2s2ehx20XFB7tCZx";
$conndb = mysql_pconnect($hostname, $username, $password) or trigger_error(mysql_error());
?>