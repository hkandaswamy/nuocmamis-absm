<?php
require_once('database.php');

function getID() {
    global $database;
    global $conndb;

    $sql = "SELECT * FROM ID ORDER BY name ASC";
    mysql_select_db($database, $conndb);
    $rs = mysql_query($sql, $conndb) or die(mysql_error());
    $rows = mysql_fetch_assoc($rs);
    $tot_rows = mysql_num_rows($rs);
    if ($tot_rows > 0) {
        echo "<select name=\"srch_language\" ID=\"srch_language\" Name=\"srch_language\">\n";
        echo "<option value=\"\">Any language&hellip;</option>\n";
        do {
            echo "<option value=\"".$rows['ID']."\">".$rows['Name']."</option>";
        } while($rows = mysql_fetch_assoc($rs));
        echo "</select>";
    }
    mysql_free_result($rs);
}

function get() {
    global $database;
    global $conndb;

    $sql = "SELECT * FROM ID ORDER BY name ASC";
    mysql_select_db($database, $conndb);
    $rs = mysql_query($sql, $conndb) or die(mysql_error());
    $rows = mysql_fetch_assoc($rs);
    $tot_rows = mysql_num_rows($rs);
    if ($tot_rows > 0) {
        echo "<select name=\"srch_language\" ID=\"srch_language\" Name=\"srch_language\">\n";
        echo "<option value=\"\">Any language&hellip;</option>\n";
        do {
            echo "<option value=\"".$rows['ID']."\">".$rows['Name']."</option>";
        } while($rows = mysql_fetch_assoc($rs));
        echo "</select>";
    }
    mysql_free_result($rs);
}
?>
