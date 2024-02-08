<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Погода из базы данных</title>
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            background-color: #00bfff;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 10px;
            color: blue;
        }
        h2 {
            text-align: center;
            color: blue;
        }
    </style>
</head>
<body>

<h2>Погода из базы данных</h2>

<?php
$servername = "mariadb"; // Имя сервиса MariaDB в сети Docker Compose
$username = "sergey";
$password = "1111";
$dbname = "weather_sergey";

// Создание подключения
$conn = new mysqli($servername, $username, $password, $dbname);

// Проверка соединения
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$conn->set_charset("utf8mb4");

echo "Ниже представлена погода из базы данных";
?>

<?php
// SQL-запрос
"SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Вывод данных в виде HTML-таблицы
    echo "<table><tr><th>ID</th><th>City</th><th>Temperature</th><th>Feels Like</th><th>Timestamp</th></tr>";
    // Вывод каждой строки данных
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>".$row["id"]."</td><td>".$row["city"]."</td><td>".$row["temperature"]."</td><td>".$row["feels_like"]."</td><td>".$row["timestamp"]."</td></tr>";
    }
    echo "</table>";
} else {
    echo "0 результатов";
}
$conn->close();
?>

</body>
</html>