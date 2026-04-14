<?php
$username=$_POST['username'];
$email =  $_POST['email'];
$pass =  $_POST['password'] ; 
$ok = true;
$messages = array();
 $conn = mysqli_connect("localhost", "root", "","registration");
// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
// echo 'Connected successfully';

$query = "SELECT 'email' FROM  `users` WHERE email = '".$email."'";
$result = mysqli_query($conn, $query);
if (mysqli_num_rows($result) > 0) {
  $ok = false;
  $messages[] = 'Email already exists!';
} else {
    $sql = "INSERT INTO users (email, name, password)
    VALUES ( '$email','$username', '$pass')";
    if (mysqli_query($conn, $sql)) {
        // echo "New record created successfully";
        $ok = true;
        $messages[] = 'New record created successfully!';
      } else {
        // echo "Error: " . $sql . "<br>" . mysqli_error($conn);
        $ok = false;
        $messages[] = 'Cannot create the record!';
      }
      
}
echo json_encode(
  array(
      'ok' => $ok,
      'messages' => $messages
  )
);
mysqli_close($conn);
?>