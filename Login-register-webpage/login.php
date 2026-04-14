<?php
 $email =  $_POST['loginEmail'];
 $pass =  $_POST['loginPassword'] ; 
 $conn = mysqli_connect("localhost", "root", "","registration");
// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
// echo 'Connected successfully';

$query = "SELECT * FROM  `users` WHERE email = '".$email."'";
$result = mysqli_query($conn, $query);

if (mysqli_num_rows($result) > 0) {
    $row= mysqli_fetch_assoc($result);
    if ($row["password"]== $pass) {
        // output data of each row
        echo( "Welcome {$row["name"]}");
        header("Location: dashboard.html?username={$row["name"]}");
      } else {
        // echo "Invalid email or password!";
        header("Location: index.html?message=Invalid email or password!");
      }
} else {
  header("Location: index.html?message=Invalid email or password!");
}
mysqli_close($conn);
exit;
?>