-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: watermanagement
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `company_information`
--

DROP TABLE IF EXISTS `company_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_information` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_logo` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `company_address` varchar(255) DEFAULT NULL,
  `company_email` varchar(255) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `company_website_url` varchar(255) DEFAULT NULL,
  `company_description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_information`
--

LOCK TABLES `company_information` WRITE;
/*!40000 ALTER TABLE `company_information` DISABLE KEYS */;
INSERT INTO `company_information` VALUES (1,'/static/uploads/tmp/company_logo.png','Dakoke Springs','82 Osupuko, Ongata Rongai','info@dakokesprings.co.ke','254720352846','https://dakokesprings.co.ke','Dakoke Springs is dedicated to providing clean and accessible water solutions for everyone, ensuring a healthier and more sustainable future.');
/*!40000 ALTER TABLE `company_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `message` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expense`
--

DROP TABLE IF EXISTS `expense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expense` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `expense_type` varchar(255) NOT NULL,
  `vendor` varchar(255) NOT NULL,
  `amount` float NOT NULL,
  `description` text NOT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `expense_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expense`
--

LOCK TABLES `expense` WRITE;
/*!40000 ALTER TABLE `expense` DISABLE KEYS */;
/*!40000 ALTER TABLE `expense` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mail_settings`
--

DROP TABLE IF EXISTS `mail_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mail_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mail_server` varchar(120) DEFAULT NULL,
  `company_email` varchar(120) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mail_settings`
--

LOCK TABLES `mail_settings` WRITE;
/*!40000 ALTER TABLE `mail_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `mail_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `content` text NOT NULL,
  `timestamp` datetime NOT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sender_id` (`sender_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,20,1,'hello there','2024-05-01 23:04:37',0),(2,20,1,'have you completed the meter readings','2024-05-01 23:04:51',0);
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meter_reading`
--

DROP TABLE IF EXISTS `meter_reading`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meter_reading` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `customer_name` varchar(50) DEFAULT NULL,
  `house_section` varchar(50) DEFAULT NULL,
  `house_number` varchar(20) DEFAULT NULL,
  `reading_value` float DEFAULT NULL,
  `consumed` float DEFAULT NULL,
  `unit_price` float DEFAULT NULL,
  `service_fee` float DEFAULT NULL,
  `sub_total_amount` float DEFAULT NULL,
  `total_amount` float DEFAULT NULL,
  `payment_status` tinyint(1) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `meter_reading_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=293 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meter_reading`
--

LOCK TABLES `meter_reading` WRITE;
/*!40000 ALTER TABLE `meter_reading` DISABLE KEYS */;
INSERT INTO `meter_reading` VALUES (15,'2024-01-30 23:55:46','peter kihiu','osupuko','1',92,92,100,0,9200,9200,1,2),(16,'2024-01-30 23:56:22','jilo guyo','osupuko','12',67,67,100,0,6700,6700,1,15),(17,'2024-01-30 23:56:43','susan karongo','osupuko','19',81,81,100,0,8100,8100,1,10),(18,'2024-01-30 23:57:19','Robert leteipa','osupuko','21',0,0,100,0,0,0,1,17),(19,'2024-01-30 23:59:07','ruth vulimu','osupuko','44',0,0,100,0,0,0,1,16),(20,'2024-01-30 23:59:37','Jeremiah kariuki','osupuko','46',151,151,100,0,15100,15100,1,14),(22,'2024-01-31 00:00:45','hezekiel ombima','osupuko','55',32,32,100,0,3200,3200,1,5),(23,'2024-01-31 00:01:07','newton njeru','osupuko','56',103,103,100,0,10300,10300,1,18),(24,'2024-01-31 00:01:39','leah kubai','osupuko','57',20,20,100,0,2000,2000,1,19),(25,'2024-01-31 00:02:28','christina christina','osupuko','61',182,182,100,0,18200,18200,1,9),(26,'2024-01-31 00:03:08','Eldiadia mageni','osupuko','76',163,163,100,0,16300,16300,1,11),(27,'2024-01-31 00:07:59','roman hinga','osupuko','79',60,60,100,0,6000,6000,1,13),(28,'2024-01-31 00:08:30','Hellen marambii','osupuko','81',115,115,100,0,11500,11500,1,8),(29,'2024-01-31 00:09:02','Komi Komi','phase 3','1',157,157,100,0,15700,15700,1,6),(30,'2024-01-31 00:09:39','Pamela Njage','villa','1',115,115,100,0,11500,11500,1,3),(31,'2024-01-31 00:10:01','emily akuno','villa','5',46,46,100,0,4600,4600,1,12),(32,'2024-01-31 00:12:24','Guadenicia Guadenicia','villa','2',22,22,100,0,2200,2200,1,4),(34,'2024-01-31 00:15:47','Raphael Koome','osupuko','52',0,0,100,0,0,0,1,7),(36,'2024-02-28 00:28:01','peter kihiu','osupuko','1',92,0,100,0,0,0,1,2),(37,'2024-02-28 00:28:46','jilo guyo','osupuko','12',80,13,100,0,1300,1300,1,15),(38,'2024-02-28 00:29:03','susan karongo','osupuko','19',90,9,100,0,900,900,1,10),(39,'2024-02-28 00:29:27','Robert leteipa','osupuko','21',83,83,100,0,8300,8300,1,17),(40,'2024-02-28 00:29:54','ruth vulimu','osupuko','44',127,127,100,0,12700,12700,1,16),(41,'2024-02-28 00:30:16','Jeremiah kariuki','osupuko','46',159,8,100,0,800,800,1,14),(42,'2024-02-28 00:30:50','Raphael Koome','osupuko','52',0,0,100,0,0,0,1,7),(43,'2024-02-28 00:31:17','hezekiel ombima','osupuko','55',32,0,100,0,0,0,1,5),(44,'2024-02-28 00:32:09','leah kubai','osupuko','57',21,1,100,0,100,100,1,19),(45,'2024-02-28 00:33:26','christina christina','osupuko','61',222,40,100,0,4000,4000,1,9),(46,'2024-02-28 00:34:07','Eldiadia mageni','osupuko','76',167,4,100,0,400,400,1,11),(47,'2024-02-28 00:35:00','roman hinga','osupuko','79',70,10,100,0,1000,1000,1,13),(48,'2024-02-28 00:35:30','Hellen marambii','osupuko','81',124,9,100,0,900,900,1,8),(49,'2024-02-28 00:37:40','Komi Komi','phase 3','1',176,19,100,0,1900,1900,1,6),(50,'2024-02-28 00:38:05','Pamela Njage','villa','1',137,22,100,0,2200,2200,1,3),(51,'2024-02-28 00:38:25','emily akuno','villa','5',72,26,100,0,2600,2600,1,12),(52,'2024-02-28 00:39:02','Guadenicia Guadenicia','villa','2',35,13,100,0,1300,1300,1,4),(56,'2024-03-27 01:15:41','peter kihiu','osupuko','1',101,9,100,0,900,900,1,2),(57,'2024-03-27 01:17:02','jilo guyo','osupuko','12',96,16,100,0,1600,1600,1,15),(58,'2024-03-27 01:17:33','susan karongo','osupuko','19',90,0,100,0,0,0,1,10),(59,'2024-03-27 01:18:09','Robert leteipa','osupuko','21',88,5,100,0,500,500,1,17),(60,'2024-03-27 01:19:02','ruth vulimu','osupuko','44',133,6,100,0,600,600,1,16),(61,'2024-03-27 01:19:35','Jeremiah kariuki','osupuko','46',161,2,100,0,200,200,1,14),(62,'2024-03-27 01:25:49','hezekiel ombima','osupuko','55',32,0,100,0,0,0,1,5),(63,'2024-03-27 01:28:51','leah kubai','osupuko','57',21,0,100,0,0,0,1,19),(64,'2024-03-27 01:29:18','christina christina','osupuko','61',252,30,100,0,3000,3000,1,9),(65,'2024-03-27 01:29:52','Eldiadia mageni','osupuko','76',170,3,100,0,300,300,1,11),(66,'2024-03-27 01:32:15','Komi Komi','phase 3','1',191,15,100,0,1500,1500,1,6),(67,'2024-03-27 01:33:29','Pamela Njage','villa','1',163,26,100,0,2600,2600,1,3),(68,'2024-03-27 01:33:54','emily akuno','villa','5',89,17,100,0,1700,1700,1,12),(69,'2024-03-27 01:34:13','Guadenicia Guadenicia','villa','2',42,7,100,0,700,700,1,4),(74,'2024-01-28 12:26:17','david ngwirii','osupuko','6',649,649,100,0,64900,64900,1,21),(75,'2024-01-28 12:28:26','rose osogo','osupuko','9',0,0,100,0,0,0,1,22),(76,'2024-01-28 12:30:23','andrew akoko','osupuko','11',103,103,100,0,10300,10300,1,23),(77,'2024-01-28 12:31:28','rodgers mutai','osupuko','14',343,343,100,0,34300,34300,1,24),(78,'2024-01-28 12:32:11','cynthia oliwa','osupuko','16',85,85,100,0,8500,8500,1,25),(79,'2024-01-28 12:33:32','simon mwilu','osupuko','17',53,53,100,0,5300,5300,1,26),(80,'2024-01-28 12:33:57','evelyn onamu','osupuko','20',81,81,100,0,8100,8100,1,27),(81,'2024-01-28 12:34:20','ibrahim onyatta','osupuko','22',74,74,100,0,7400,7400,1,28),(82,'2024-01-28 12:34:41','kiragu maina','osupuko','23',65,65,100,0,6500,6500,1,29),(83,'2024-01-28 12:35:31','joanne joanne','osupuko','24',234,234,100,0,23400,23400,1,30),(84,'2024-01-28 12:35:54','Elizabeth kamweru','osupuko','25',64,64,100,0,6400,6400,1,31),(85,'2024-01-28 12:36:59','maria maria','osupuko','27',304,304,100,0,30400,30400,1,32),(86,'2024-01-28 12:37:35','george ogwang','osupuko','48',32,32,100,0,3200,3200,1,33),(87,'2024-01-28 12:38:05','lillian omosa','osupuko','49',0,0,100,0,0,0,1,34),(88,'2024-01-28 12:38:42','stephen ngwer (neville)','osupuko','50',147,147,100,0,14700,14700,1,35),(89,'2024-01-28 12:39:33','abanga abanga','osupuko','51',134,134,100,0,13400,13400,1,36),(90,'2024-01-28 12:40:06','brian muturi','osupuko','54',292,292,100,0,29200,29200,1,37),(91,'2024-01-28 12:40:27','lydia njuguna','osupuko','58',112,112,100,0,11200,11200,1,38),(92,'2024-01-28 12:40:57','geoffrey malakweny','osupuko','59',83,83,100,0,8300,8300,1,39),(93,'2024-01-28 12:41:45','steve odinyo','osupuko','60',251,251,100,0,25100,25100,1,40),(94,'2024-01-28 12:42:17','beatrice okundi','osupuko','62',110,110,100,0,11000,11000,1,41),(95,'2024-01-28 12:42:53','george ambatta','osupuko','63',410,410,100,0,41000,41000,1,42),(96,'2024-01-28 12:43:25','colette aloo','osupuko','64',35,35,100,0,3500,3500,1,43),(97,'2024-01-28 12:43:46','irene irene','osupuko','65',0,0,100,0,0,0,1,44),(98,'2024-01-28 12:44:48','ann kamau','osupuko','66',209,209,100,0,20900,20900,1,45),(99,'2024-01-28 12:45:12','erick korir','osupuko','67',309,309,100,0,30900,30900,1,46),(100,'2024-01-28 12:45:42','martha nyambura','osupuko','72',130,130,100,0,13000,13000,1,47),(101,'2024-01-28 12:46:11','kankano robert','osupuko','73',238,238,100,0,23800,23800,1,48),(102,'2024-01-28 12:47:35','catherine james','osupuko','74',69,69,100,0,6900,6900,1,49),(103,'2024-01-28 12:48:13','george juma','osupuko','78',151,151,100,0,15100,15100,1,50),(104,'2024-01-28 12:48:50','jerusha mwenda','osupuko','80',71,71,100,0,7100,7100,1,51),(105,'2024-01-28 12:50:13','lukas leboo','chui lane','1',272,272,100,0,27200,27200,1,52),(106,'2024-01-28 12:51:03','daniel mburu','chui lane','2',140,140,100,0,14000,14000,1,53),(107,'2024-01-28 12:51:48','ricahrd wanjiku','phase 3','2',321,321,100,0,32100,32100,1,54),(108,'2024-01-28 12:53:18','grace mburu','phase 3','3',31,31,100,0,3100,3100,1,55),(109,'2024-01-28 12:53:43','newton njeru','phase 3','4',126,126,100,0,12600,12600,1,56),(110,'2024-01-28 12:54:12','benjamin okeyo','villa','3',206,206,100,0,20600,20600,1,57),(111,'2024-01-28 12:55:00','phyllis barasa','villa','9',139,139,100,0,13900,13900,1,58),(112,'2024-01-28 12:55:32','truphosa okwar','villa','10',302,302,100,0,30200,30200,1,59),(114,'2024-02-29 13:24:30','david ngwirii','osupuko','6',672,23,100,0,2300,2300,1,21),(115,'2024-02-29 13:25:15','rose osogo','osupuko','9',8,8,100,0,800,800,1,22),(116,'2024-02-29 13:25:47','andrew akoko','osupuko','11',110,7,100,0,700,700,1,23),(117,'2024-02-29 13:31:09','cynthia oliwa','osupuko','16',92,7,100,0,700,700,1,25),(118,'2024-02-29 13:31:16','rodgers mutai','osupuko','14',364,21,100,0,2100,2100,1,24),(119,'2024-02-29 13:31:48','simon mwilu','osupuko','17',57,4,100,0,400,400,1,26),(120,'2024-02-29 13:32:18','evelyn onamu','osupuko','20',84,3,100,0,300,300,1,27),(121,'2024-02-29 13:32:42','ibrahim onyatta','osupuko','22',74,0,100,0,0,0,1,28),(122,'2024-02-29 13:33:03','kiragu maina','osupuko','23',82,17,100,0,1700,1700,1,29),(123,'2024-02-29 13:33:46','joanne joanne','osupuko','24',243,9,100,0,900,900,1,30),(124,'2024-02-29 13:34:53','Elizabeth kamweru','osupuko','25',80,16,100,0,1600,1600,1,31),(125,'2024-02-29 13:35:11','maria maria','osupuko','27',304,0,100,0,0,0,1,32),(126,'2024-02-29 13:35:32','george ogwang','osupuko','48',37,5,100,0,500,500,1,33),(127,'2024-02-29 13:36:08','lillian omosa','osupuko','49',0,0,100,0,0,0,1,34),(128,'2024-02-29 13:38:15','stephen ngwer (neville)','osupuko','50',147,0,100,0,0,0,1,35),(129,'2024-02-29 13:38:36','abanga abanga','osupuko','51',150,16,100,0,1600,1600,1,36),(130,'2024-02-29 13:39:09','brian muturi','osupuko','54',354,62,100,0,6200,6200,1,37),(131,'2024-02-29 13:39:32','lydia njuguna','osupuko','58',120,8,100,0,800,800,1,38),(132,'2024-02-29 13:40:00','geoffrey malakweny','osupuko','59',92,9,100,0,900,900,1,39),(133,'2024-02-29 13:40:41','steve odinyo','osupuko','60',270,19,100,0,1900,1900,1,40),(134,'2024-02-29 13:41:04','beatrice okundi','osupuko','62',127,17,100,0,1700,1700,1,41),(135,'2024-02-29 13:41:35','george ambatta','osupuko','63',414,4,100,0,400,400,1,42),(136,'2024-02-29 13:42:01','colette aloo','osupuko','64',48,13,100,0,1300,1300,1,43),(137,'2024-02-29 13:42:38','irene irene','osupuko','65',77,77,100,0,7700,7700,1,44),(138,'2024-02-29 13:43:23','ann kamau','osupuko','66',227,18,100,0,1800,1800,1,45),(139,'2024-02-29 13:43:48','erick korir','osupuko','67',327,18,100,0,1800,1800,1,46),(140,'2024-02-29 13:44:16','martha nyambura','osupuko','72',152,22,100,0,2200,2200,1,47),(141,'2024-02-29 13:44:50','kankano robert','osupuko','73',291,53,100,0,5300,5300,1,48),(142,'2024-02-29 13:46:07','catherine james','osupuko','74',80,11,100,0,1100,1100,1,49),(143,'2024-02-29 13:46:39','george juma','osupuko','78',189,38,100,0,3800,3800,1,50),(144,'2024-02-29 13:48:05','jerusha mwenda','osupuko','80',71,0,100,0,0,0,1,51),(145,'2024-02-29 13:48:59','lukas leboo','chui lane','1',317,45,100,0,4500,4500,1,52),(146,'2024-02-29 13:50:14','daniel mburu','chui lane','2',175,35,100,0,3500,3500,1,53),(147,'2024-02-29 13:50:39','ricahrd wanjiku','phase 3','2',408,87,100,0,8700,8700,1,54),(148,'2024-02-29 13:51:15','grace mburu','phase 3','3',36,5,100,0,500,500,1,55),(149,'2024-02-29 13:51:33','newton njeru','phase 3','4',151,25,100,0,2500,2500,1,56),(150,'2024-02-29 13:51:57','benjamin okeyo','villa','3',230,24,100,0,2400,2400,1,57),(151,'2024-02-29 13:52:29','phyllis barasa','villa','9',151,12,100,0,1200,1200,1,58),(152,'2024-02-29 13:52:47','truphosa okwar','villa','10',326,24,100,0,2400,2400,1,59),(153,'2024-02-29 13:53:29','cynthia oliwa','osupuko','16',92,0,100,0,0,0,1,25),(154,'2024-03-29 14:01:28','david ngwirii','osupuko','6',867,195,100,0,19500,19500,1,21),(155,'2024-03-29 14:02:14','rose osogo','osupuko','9',15,7,100,0,700,700,1,22),(156,'2024-03-29 14:02:32','andrew akoko','osupuko','11',114,4,100,0,400,400,1,23),(157,'2024-03-29 14:02:52','rodgers mutai','osupuko','14',371,7,100,0,700,700,1,24),(158,'2024-03-29 14:03:15','cynthia oliwa','osupuko','16',98,6,100,0,600,600,1,25),(159,'2024-03-29 14:03:36','simon mwilu','osupuko','17',64,7,100,0,700,700,1,26),(160,'2024-03-29 14:03:53','evelyn onamu','osupuko','20',91,7,100,0,700,700,1,27),(161,'2024-03-29 14:04:28','ibrahim onyatta','osupuko','22',108,34,100,0,3400,3400,1,28),(162,'2024-03-29 14:04:50','kiragu maina','osupuko','23',90,8,100,0,800,800,1,29),(163,'2024-03-29 14:05:17','joanne joanne','osupuko','24',243,0,100,0,0,0,1,30),(164,'2024-03-29 14:06:14','Elizabeth kamweru','osupuko','25',93,13,100,0,1300,1300,1,31),(165,'2024-03-29 14:06:44','maria maria','osupuko','27',315,11,100,0,1100,1100,1,32),(166,'2024-03-29 14:07:07','george ogwang','osupuko','48',37,0,100,0,0,0,1,33),(167,'2024-03-29 14:08:57','lillian omosa','osupuko','49',0,0,100,0,0,0,1,34),(168,'2024-03-29 14:09:15','stephen ngwer (neville)','osupuko','50',209,62,100,0,6200,6200,1,35),(169,'2024-03-29 14:09:38','abanga abanga','osupuko','51',158,8,100,0,800,800,1,36),(170,'2024-03-29 14:09:57','brian muturi','osupuko','54',393,39,100,0,3900,3900,1,37),(171,'2024-03-29 14:13:31','lydia njuguna','osupuko','58',120,0,100,0,0,0,1,38),(172,'2024-03-29 14:15:37','geoffrey malakweny','osupuko','59',92,0,100,0,0,0,1,39),(173,'2024-03-29 14:16:03','steve odinyo','osupuko','60',271,1,100,0,100,100,1,40),(174,'2024-03-29 14:16:35','beatrice okundi','osupuko','62',141,14,100,0,1400,1400,1,41),(175,'2024-03-29 14:17:04','george ambatta','osupuko','63',415,1,100,0,100,100,1,42),(176,'2024-03-29 14:17:36','colette aloo','osupuko','64',54,6,100,0,600,600,1,43),(177,'2024-03-29 14:17:59','irene irene','osupuko','65',77,0,100,0,0,0,1,44),(178,'2024-03-29 14:18:22','ann kamau','osupuko','66',242,15,100,0,1500,1500,1,45),(179,'2024-03-29 14:18:47','erick korir','osupuko','67',344,17,100,0,1700,1700,1,46),(180,'2024-03-29 14:19:08','martha nyambura','osupuko','72',167,15,100,0,1500,1500,1,47),(181,'2024-03-29 14:19:28','kankano robert','osupuko','73',291,0,100,0,0,0,1,48),(182,'2024-03-29 14:19:52','george juma','osupuko','78',211,22,100,0,2200,2200,1,50),(183,'2024-03-29 14:20:14','jerusha mwenda','osupuko','80',92,21,100,0,2100,2100,1,51),(184,'2024-03-29 14:20:40','lukas leboo','chui lane','1',354,37,100,0,3700,3700,1,52),(185,'2024-03-29 14:20:57','daniel mburu','chui lane','2',192,17,100,0,1700,1700,1,53),(186,'2024-03-29 14:21:24','ricahrd wanjiku','phase 3','2',439,31,100,0,3100,3100,1,54),(187,'2024-03-29 14:21:58','grace mburu','phase 3','3',40,4,100,0,400,400,1,55),(188,'2024-03-29 14:22:23','newton njeru','phase 3','4',171,20,100,0,2000,2000,1,56),(189,'2024-03-29 14:22:46','benjamin okeyo','villa','3',254,24,100,0,2400,2400,1,57),(190,'2024-03-29 14:24:22','phyllis barasa','villa','9',169,18,100,0,1800,1800,1,58),(191,'2024-03-29 14:24:45','truphosa okwar','villa','10',360,34,100,0,3400,3400,1,59),(243,'2024-04-29 01:04:52','peter kihiu','osupuko','1',115,14,130,200,1820,2020,0,2),(244,'2024-04-29 01:05:30','david ngwirii','osupuko','6',1019,152,130,200,19760,19960,0,21),(245,'2024-04-29 01:05:58','andrew akoko','osupuko','11',119,5,130,200,650,850,0,23),(246,'2024-04-29 01:06:48','jilo guyo','osupuko','12',107,11,130,200,1430,1630,0,15),(249,'2024-04-29 01:11:37','rodgers mutai','osupuko','14',384,13,130,200,1690,1890,0,24),(250,'2024-04-29 01:12:00','cynthia oliwa','osupuko','16',98,0,130,200,0,200,0,25),(251,'2024-04-29 01:12:17','simon mwilu','osupuko','17',65,1,130,200,130,330,1,26),(252,'2024-04-29 01:12:38','susan karongo','osupuko','19',90,0,130,200,0,200,0,10),(253,'2024-04-29 01:12:59','evelyn onamu','osupuko','20',98,7,130,200,910,1110,0,27),(254,'2024-04-29 01:13:16','Robert leteipa','osupuko','21',89,1,130,200,130,330,0,17),(255,'2024-04-29 01:13:31','ibrahim onyatta','osupuko','22',117,9,130,200,1170,1370,0,28),(256,'2024-04-29 01:13:55','kiragu maina','osupuko','23',91,1,130,200,130,330,0,29),(257,'2024-04-29 01:14:15','Elizabeth kamweru','osupuko','25',109,16,130,200,2080,2280,0,31),(258,'2024-04-29 01:14:37','maria maria','osupuko','27',325,10,130,200,1300,1500,0,32),(259,'2024-04-29 01:15:03','ruth vulimu','osupuko','44',139,6,130,200,780,980,0,16),(260,'2024-04-29 01:15:35','Jeremiah kariuki','osupuko','46',161,0,130,200,0,200,0,14),(261,'2024-04-29 01:15:59','abanga abanga','osupuko','51',175,17,130,200,2210,2410,0,36),(262,'2024-04-29 01:16:18','brian muturi','osupuko','54',432,39,130,200,5070,5270,0,37),(263,'2024-04-29 01:16:37','hezekiel ombima','osupuko','55',32,0,130,200,0,200,0,5),(264,'2024-04-29 01:19:54','leah kubai','osupuko','57',21,0,130,200,0,200,0,19),(265,'2024-04-29 01:20:54','lydia njuguna','osupuko','58',137,17,130,200,2210,2410,0,38),(266,'2024-04-29 01:21:11','steve odinyo','osupuko','60',271,0,130,200,0,200,0,40),(267,'2024-04-29 01:21:38','christina christina','osupuko','61',272,20,130,200,2600,2800,0,9),(268,'2024-04-29 01:22:05','george ambatta','osupuko','63',415,0,130,200,0,200,0,42),(269,'2024-04-29 01:22:24','colette aloo','osupuko','64',54,0,130,200,0,200,0,43),(270,'2024-04-29 01:22:56','ann kamau','osupuko','66',264,22,130,200,2860,3060,0,45),(271,'2024-04-29 01:23:25','erick korir','osupuko','67',357,13,130,200,1690,1890,0,46),(272,'2024-04-29 01:23:47','kankano robert','osupuko','73',291,0,130,200,0,200,0,48),(273,'2024-04-29 01:24:04','catherine james','osupuko','74',100,20,130,200,2600,2800,0,49),(274,'2024-04-29 01:24:24','Eldiadia mageni','osupuko','76',170,0,130,200,0,200,0,11),(275,'2024-04-29 01:25:49','roman hinga','osupuko','79',71,1,130,200,130,330,0,13),(276,'2024-04-29 01:27:38','Hellen marambii','osupuko','81',125,1,130,200,130,330,0,8),(277,'2024-04-29 01:28:02','lukas leboo','chui lane','1',388,34,130,200,4420,4620,0,52),(278,'2024-04-29 01:28:53','daniel mburu','chui lane','2',197,5,130,200,650,850,0,53),(279,'2024-04-29 01:29:47','Komi Komi','phase 3','1',207,16,130,200,2080,2280,0,6),(280,'2024-04-29 01:30:38','grace mburu','phase 3','3',46,6,130,200,780,980,0,55),(281,'2024-04-29 01:31:58','newton njeru','phase 3','4',172,1,130,200,130,330,0,56),(282,'2024-04-29 01:32:47','Pamela Njage','villa','1',194,31,130,200,4030,4230,0,3),(283,'2024-04-29 01:33:21','benjamin okeyo','villa','3',279,25,130,200,3250,3450,0,57),(284,'2024-04-29 01:33:46','emily akuno','villa','5',101,12,130,200,1560,1760,0,12),(285,'2024-04-29 01:34:55','phyllis barasa','villa','9',182,13,130,200,1690,1890,0,58),(286,'2024-04-29 01:35:27','truphosa okwar','villa','10',367,7,130,200,910,1110,0,59),(287,'2024-04-29 01:36:04','Guadenicia Guadenicia','villa','2',58,16,130,200,2080,2280,0,4),(288,'2024-04-29 01:29:47','ricahrd wanjiku','phase 3','2',0,0,130,200,200,200,0,54),(289,'2024-01-31 01:29:47','michael michael','osupuko','15',40,40,100,0,4000,4000,1,60),(290,'2024-02-29 01:29:47','michael michael','osupuko','15',66,26,100,0,2600,2600,1,60),(291,'2024-03-29 01:29:47','michael michael','osupuko','15',110,44,100,0,4400,4400,1,60),(292,'2024-04-29 01:29:47','michael michael','osupuko','15',156,46,130,200,5980,5980,0,60);
/*!40000 ALTER TABLE `meter_reading` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `note`
--

DROP TABLE IF EXISTS `note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `note` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `note_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `note`
--

LOCK TABLES `note` WRITE;
/*!40000 ALTER TABLE `note` DISABLE KEYS */;
/*!40000 ALTER TABLE `note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_reset_token`
--

DROP TABLE IF EXISTS `password_reset_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_reset_token` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `token` varchar(128) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_reset_token`
--

LOCK TABLES `password_reset_token` WRITE;
/*!40000 ALTER TABLE `password_reset_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_reset_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_amount` int DEFAULT NULL,
  `customer_name` varchar(50) DEFAULT NULL,
  `amount` float NOT NULL,
  `timestamp` datetime NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `reference_number` varchar(50) DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `user_id` int NOT NULL,
  `invoice_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `invoice_id` (`invoice_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`invoice_id`) REFERENCES `meter_reading` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,2200,'Guadenicia Guadenicia',2200,'2024-02-28 00:18:29','m_pesa','',0,4,32),(2,4600,'emily akuno',4600,'2024-02-28 00:18:38','m_pesa','',0,12,31),(3,11500,'Pamela Njage',11500,'2024-02-28 00:18:47','m_pesa','',0,3,30),(4,15700,'Komi Komi',15700,'2024-02-28 00:18:59','m_pesa','',0,6,29),(5,11500,'Hellen marambii',11500,'2024-02-28 00:19:13','m_pesa','',0,8,28),(6,6000,'roman hinga',6000,'2024-02-28 00:19:23','m_pesa','',0,13,27),(7,16300,'Eldiadia mageni',16300,'2024-02-28 00:19:33','m_pesa','',0,11,26),(8,18200,'christina christina',18200,'2024-02-28 00:19:41','m_pesa','',0,9,25),(9,2000,'leah kubai',2000,'2024-02-28 00:19:51','m_pesa','',0,19,24),(10,10300,'newton njeru',10300,'2024-02-28 00:20:29','m_pesa','',0,18,23),(11,3200,'hezekiel ombima',3200,'2024-02-28 00:20:40','m_pesa','',0,5,22),(12,15100,'Jeremiah kariuki',15100,'2024-02-28 00:20:48','m_pesa','',0,14,20),(13,8100,'susan karongo',8100,'2024-02-28 00:20:57','m_pesa','',0,10,17),(14,6700,'jilo guyo',6700,'2024-02-28 00:21:17','m_pesa','',0,15,16),(15,9200,'peter kihiu',9200,'2024-02-28 00:21:25','m_pesa','',0,2,15),(16,1000,'roman hinga',1000,'2024-03-27 18:33:22','m_pesa','',0,13,47),(17,700,'Guadenicia Guadenicia',700,'2024-03-27 18:33:40','m_pesa','',0,4,69),(18,1300,'jilo guyo',1300,'2024-03-27 18:33:55','m_pesa','',0,15,37),(19,900,'susan karongo',900,'2024-03-27 18:34:08','m_pesa','',0,10,38),(20,8300,'Robert leteipa',8300,'2024-03-27 18:34:23','m_pesa','',0,17,39),(21,12700,'ruth vulimu',12700,'2024-03-27 18:34:40','m_pesa','',0,16,40),(22,800,'Jeremiah kariuki',800,'2024-03-27 18:34:53','m_pesa','',0,14,41),(23,4000,'christina christina',4000,'2024-03-27 18:35:09','m_pesa','',0,9,45),(24,100,'leah kubai',100,'2024-03-27 18:35:24','m_pesa','',0,19,44),(25,400,'Eldiadia mageni',400,'2024-03-27 18:35:38','m_pesa','',0,11,46),(26,900,'Hellen marambii',900,'2024-03-27 18:35:49','m_pesa','',0,8,48),(27,1900,'Komi Komi',1900,'2024-03-27 18:36:04','m_pesa','',0,6,49),(28,2200,'Pamela Njage',2200,'2024-03-27 18:36:17','m_pesa','',0,3,50),(29,2600,'emily akuno',2600,'2024-03-27 18:36:36','m_pesa','',0,12,51),(30,1300,'Guadenicia Guadenicia',1300,'2024-03-27 18:36:53','m_pesa','',0,4,52),(31,900,'peter kihiu',900,'2024-03-27 18:37:24','m_pesa','',0,2,56),(32,1600,'jilo guyo',1600,'2024-03-27 18:37:37','m_pesa','',0,15,57),(33,500,'Robert leteipa',500,'2024-03-27 18:37:52','m_pesa','',0,17,59),(34,600,'ruth vulimu',600,'2024-03-27 18:38:03','m_pesa','',0,16,60),(35,200,'Jeremiah kariuki',200,'2024-03-27 18:38:41','m_pesa','',0,14,61),(36,3000,'christina christina',3000,'2024-03-27 18:38:53','m_pesa','',0,9,64),(37,300,'Eldiadia mageni',300,'2024-03-27 18:39:08','m_pesa','',0,11,65),(38,1500,'Komi Komi',1500,'2024-03-27 18:39:21','m_pesa','',0,6,66),(39,2600,'Pamela Njage',2600,'2024-03-27 18:39:33','m_pesa','',0,3,67),(40,1700,'emily akuno',1700,'2024-03-27 18:39:43','m_pesa','',0,12,68),(41,30200,'truphosa okwar',30200,'2024-01-28 12:58:20','m_pesa','',0,59,112),(42,13900,'phyllis barasa',13900,'2024-01-28 12:58:29','m_pesa','',0,58,111),(43,20600,'benjamin okeyo',20600,'2024-01-28 12:58:40','m_pesa','',0,57,110),(44,12600,'newton njeru',12600,'2024-01-28 12:59:11','m_pesa','',0,56,109),(45,3100,'grace mburu',3100,'2024-01-28 12:59:25','m_pesa','',0,55,108),(46,32100,'ricahrd wanjiku',32100,'2024-01-28 12:59:36','m_pesa','',0,54,107),(47,14000,'daniel mburu',14000,'2024-01-28 12:59:46','m_pesa','',0,53,106),(48,27200,'lukas leboo',27200,'2024-01-28 12:59:57','m_pesa','',0,52,105),(49,7100,'jerusha mwenda',7100,'2024-01-28 13:00:07','m_pesa','',0,51,104),(50,15100,'george juma',15100,'2024-01-28 13:00:19','m_pesa','',0,50,103),(51,6900,'catherine james',6900,'2024-01-28 13:00:29','m_pesa','',0,49,102),(52,23800,'kankano robert',23800,'2024-01-28 13:00:39','m_pesa','',0,48,101),(53,13000,'martha nyambura',13000,'2024-01-28 13:00:48','m_pesa','',0,47,100),(54,30900,'erick korir',30900,'2024-01-28 13:00:59','m_pesa','',0,46,99),(55,20900,'ann kamau',20900,'2024-01-28 13:01:09','m_pesa','',0,45,98),(56,3500,'colette aloo',3500,'2024-01-28 13:01:24','m_pesa','',0,43,96),(57,41000,'george ambatta',41000,'2024-01-28 13:01:33','m_pesa','',0,42,95),(58,11000,'beatrice okundi',11000,'2024-01-28 13:01:42','m_pesa','',0,41,94),(59,25100,'steve odinyo',25100,'2024-01-28 13:01:51','m_pesa','',0,40,93),(60,8300,'geoffrey malakweny',8300,'2024-01-28 13:02:02','m_pesa','',0,39,92),(61,11200,'lydia njuguna',11200,'2024-01-28 13:02:11','m_pesa','',0,38,91),(62,29200,'brian muturi',29200,'2024-01-28 13:02:21','m_pesa','',0,37,90),(63,13400,'abanga abanga',13400,'2024-01-28 13:02:29','m_pesa','',0,36,89),(64,14700,'stephen ngwer (neville)',14700,'2024-01-28 13:02:40','m_pesa','',0,35,88),(65,3200,'george ogwang',3200,'2024-01-28 13:02:53','m_pesa','',0,33,86),(66,30400,'maria maria',30400,'2024-01-28 13:03:03','m_pesa','',0,32,85),(67,6400,'Elizabeth kamweru',6400,'2024-01-28 13:03:20','m_pesa','',0,31,84),(68,23400,'joanne joanne',23400,'2024-01-28 13:03:30','m_pesa','',0,30,83),(69,6500,'kiragu maina',6500,'2024-01-28 13:03:38','m_pesa','',0,29,82),(70,7400,'ibrahim onyatta',7400,'2024-01-28 13:03:47','m_pesa','',0,28,81),(71,8100,'evelyn onamu',8100,'2024-01-28 13:03:58','m_pesa','',0,27,80),(72,5300,'simon mwilu',5300,'2024-01-28 13:04:07','m_pesa','',0,26,79),(73,8500,'cynthia oliwa',8500,'2024-01-28 13:04:15','m_pesa','',0,25,78),(74,34300,'rodgers mutai',34300,'2024-01-28 13:04:24','m_pesa','',0,24,77),(75,10300,'andrew akoko',10300,'2024-01-28 13:04:33','m_pesa','',0,23,76),(76,64900,'david ngwirii',64900,'2024-01-28 13:04:43','m_pesa','',0,21,74),(77,2300,'david ngwirii',2300,'2024-02-29 13:55:25','m_pesa','',0,21,114),(78,800,'rose osogo',800,'2024-02-29 13:55:47','m_pesa','',0,22,115),(79,700,'andrew akoko',700,'2024-02-29 13:56:11','m_pesa','',0,23,116),(80,700,'cynthia oliwa',700,'2024-02-29 13:57:28','m_pesa','',0,25,117),(81,2100,'rodgers mutai',2100,'2024-03-29 13:58:14','m_pesa','',0,24,118),(82,400,'simon mwilu',400,'2024-03-29 13:59:11','m_pesa','',0,26,119),(83,400,'simon mwilu',400,'2024-03-29 13:59:12','m_pesa','',0,26,119),(84,300,'evelyn onamu',300,'2024-03-29 13:59:47','m_pesa','',0,27,120),(85,1700,'kiragu maina',1700,'2024-03-29 14:00:43','m_pesa','',0,29,122),(86,900,'joanne joanne',900,'2024-03-29 14:02:33','m_pesa','',0,30,123),(87,1600,'Elizabeth kamweru',1600,'2024-03-29 14:03:10','m_pesa','',0,31,124),(88,500,'george ogwang',500,'2024-03-29 14:03:42','m_pesa','',0,33,126),(89,1600,'abanga abanga',1600,'2024-03-29 14:04:10','m_pesa','',0,36,129),(90,6200,'brian muturi',6200,'2024-03-29 14:04:56','m_pesa','',0,37,130),(91,800,'lydia njuguna',800,'2024-03-29 14:05:15','m_pesa','',0,38,131),(92,800,'lydia njuguna',800,'2024-03-29 14:05:15','m_pesa','',0,38,131),(93,900,'geoffrey malakweny',900,'2024-03-29 14:05:56','m_pesa','',0,39,132),(94,2400,'truphosa okwar',2400,'2024-03-29 14:06:17','m_pesa','',0,59,152),(95,1900,'steve odinyo',1900,'2024-03-29 14:06:35','m_pesa','',0,40,133),(96,1700,'beatrice okundi',1700,'2024-03-29 14:07:12','m_pesa','',0,41,134),(97,400,'george ambatta',400,'2024-03-29 14:07:39','m_pesa','',0,42,135),(98,1300,'colette aloo',1300,'2024-03-29 14:07:56','m_pesa','',0,43,136),(99,7700,'irene irene',7700,'2024-03-29 14:09:39','m_pesa','',0,44,137),(100,1800,'ann kamau',1800,'2024-03-29 14:10:24','m_pesa','',0,45,138),(101,1800,'erick korir',1800,'2024-03-29 14:11:17','m_pesa','',0,46,139),(102,2200,'martha nyambura',2200,'2024-03-29 14:12:14','m_pesa','',0,47,140),(103,5300,'kankano robert',5300,'2024-03-29 14:12:30','m_pesa','',0,48,141),(104,600,'cynthia oliwa',600,'2024-03-29 14:12:42','m_pesa','',0,25,158),(105,1100,'catherine james',1100,'2024-03-29 14:13:01','m_pesa','',0,49,142),(106,3800,'george juma',3800,'2024-03-29 14:13:18','m_pesa','',0,50,143),(107,4500,'lukas leboo',4500,'2024-03-29 14:13:40','m_pesa','',0,52,145),(108,3500,'daniel mburu',3500,'2024-03-29 14:14:02','m_pesa','',0,53,146),(109,8700,'ricahrd wanjiku',8700,'2024-03-29 14:14:17','m_pesa','',0,54,147),(110,700,'rodgers mutai',700,'2024-03-29 14:14:29','m_pesa','',0,24,157),(111,400,'andrew akoko',400,'2024-03-29 14:14:39','m_pesa','',0,23,156),(112,700,'rose osogo',700,'2024-03-29 14:14:51','m_pesa','',0,22,155),(113,19500,'david ngwirii',19500,'2024-03-29 14:15:15','m_pesa','',0,21,154),(114,1200,'phyllis barasa',1200,'2024-03-29 14:15:33','m_pesa','',0,58,151),(115,500,'grace mburu',500,'2024-03-29 14:15:49','m_pesa','',0,55,148),(116,2500,'newton njeru',2500,'2024-03-29 14:16:04','m_pesa','',0,56,149),(117,700,'simon mwilu',700,'2024-03-29 14:16:14','m_pesa','',0,26,159),(118,2400,'benjamin okeyo',2400,'2024-03-29 14:16:40','m_pesa','',0,57,150),(119,700,'evelyn onamu',700,'2024-03-29 14:17:05','m_pesa','',0,27,160),(120,3400,'ibrahim onyatta',3400,'2024-03-29 14:17:22','m_pesa','',0,28,161),(121,800,'kiragu maina',800,'2024-03-29 14:17:34','m_pesa','',0,29,162),(122,1300,'Elizabeth kamweru',1300,'2024-03-29 14:17:46','m_pesa','',0,31,164),(123,1100,'maria maria',1100,'2024-03-29 14:18:09','m_pesa','',0,32,165),(124,6200,'stephen ngwer (neville)',6200,'2024-03-29 14:18:29','m_pesa','',0,35,168),(125,800,'abanga abanga',800,'2024-03-29 14:19:05','m_pesa','',0,36,169),(126,3900,'brian muturi',3900,'2024-03-29 14:19:56','m_pesa','',0,37,170),(127,100,'steve odinyo',100,'2024-03-29 14:20:38','m_pesa','',0,40,173),(128,1400,'beatrice okundi',1400,'2024-03-29 14:20:54','m_pesa','',0,41,174),(129,100,'george ambatta',100,'2024-03-29 14:21:18','m_pesa','',0,42,175),(130,600,'colette aloo',600,'2024-03-29 14:21:30','m_pesa','',0,43,176),(131,1500,'ann kamau',1500,'2024-03-29 14:21:41','m_pesa','',0,45,178),(132,1700,'erick korir',1700,'2024-03-29 14:21:52','m_pesa','',0,46,179),(133,1500,'martha nyambura',1500,'2024-03-29 14:22:02','m_pesa','',0,47,180),(134,2200,'george juma',2200,'2024-03-29 14:22:13','m_pesa','',0,50,182),(135,2100,'jerusha mwenda',2100,'2024-03-29 14:22:23','m_pesa','',0,51,183),(136,3700,'lukas leboo',3700,'2024-03-29 14:22:35','m_pesa','',0,52,184),(137,1700,'daniel mburu',1700,'2024-03-29 14:22:53','m_pesa','',0,53,185),(138,3100,'ricahrd wanjiku',3100,'2024-03-29 14:23:34','m_pesa','',0,54,186),(139,400,'grace mburu',400,'2024-03-29 14:23:48','m_pesa','',0,55,187),(140,2000,'newton njeru',2000,'2024-03-29 14:23:59','m_pesa','',0,56,188),(141,2400,'benjamin okeyo',2400,'2024-03-29 14:25:13','m_pesa','',0,57,189),(142,1800,'phyllis barasa',1800,'2024-03-29 14:25:34','m_pesa','',0,58,190),(143,3400,'truphosa okwar',3400,'2024-03-29 14:26:06','m_pesa','',0,59,191),(144,4000,'michael michael',4000,'2024-04-29 02:28:31','m_pesa','',0,60,289),(145,2600,'michael michael',2600,'2024-04-29 02:28:54','m_pesa','',0,60,290),(146,4400,'michael michael',4400,'2024-04-29 02:29:24','m_pesa','',0,60,291);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_methods`
--

DROP TABLE IF EXISTS `payment_methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_methods` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(255) DEFAULT NULL,
  `paybill` int DEFAULT NULL,
  `account_number` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_methods`
--

LOCK TABLES `payment_methods` WRITE;
/*!40000 ALTER TABLE `payment_methods` DISABLE KEYS */;
INSERT INTO `payment_methods` VALUES (1,'Cooperative Bank',400200,40003937);
/*!40000 ALTER TABLE `payment_methods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_setting`
--

DROP TABLE IF EXISTS `services_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services_setting` (
  `id` int NOT NULL AUTO_INCREMENT,
  `unit_price` float DEFAULT NULL,
  `service_fee` float DEFAULT NULL,
  `house_sections` varchar(1050) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_setting`
--

LOCK TABLES `services_setting` WRITE;
/*!40000 ALTER TABLE `services_setting` DISABLE KEYS */;
INSERT INTO `services_setting` VALUES (1,130,200,'osupuko,chui lane,villa,phase 3,admin');
/*!40000 ALTER TABLE `services_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_accounts`
--

DROP TABLE IF EXISTS `social_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `whatsapp` varchar(255) DEFAULT NULL,
  `twitter` varchar(255) DEFAULT NULL,
  `facebook` varchar(255) DEFAULT NULL,
  `tiktok` varchar(255) DEFAULT NULL,
  `instagram` varchar(255) DEFAULT NULL,
  `linkedin` varchar(255) DEFAULT NULL,
  `youtube` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_accounts`
--

LOCK TABLES `social_accounts` WRITE;
/*!40000 ALTER TABLE `social_accounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mobile_number` varchar(20) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `house_section` varchar(50) DEFAULT NULL,
  `house_number` varchar(20) DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `balance` float DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `last_logout` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile_number` (`mobile_number`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'723396403','scrypt:32768:8:1$m5WeW4QBP22HhJRI$8fa967825223bbd31a609270cb5b9c96d1093d4dd13d58a965580285b7c00d5884676db182e0942ca207ffec2d8bb9ed13702a37c1a4e3aeb7de5ebe1b148438','main','meter','silasmungiria16@gmail.com','admin','0',NULL,1,1,0,'2024-04-30 14:10:16','2024-04-29 03:28:59'),(2,'722957502','scrypt:32768:8:1$jUihr6cfhIjHNXLQ$a2f45dfcf7874de15f9f8f6b335921833e29229bf49bd5289837c611adb734e3b68986ba6401b01abc804ffe2bc965668ed86ae7ade081fbebe86da2dcd7e859','peter','kihiu','mail@mail.com','osupuko','1',NULL,1,0,-2020,NULL,NULL),(3,'701219663','scrypt:32768:8:1$GNcx8IqDlUtJPGsX$28be4a7d1a44c6609cd884150e5f9a9c4dfabe1af851329e0b1e6260299f0056c7247361a5d47ca3657e8ec3a3f633ef434de5da572d4775ef533c4205d53d99','Pamela','Njage','mail@mail.com','villa','1',NULL,1,0,-4230,NULL,NULL),(4,'737408516','scrypt:32768:8:1$2FUP5eXg9CWh8OqH$c3631fff5b98a7f280fb9b2083e5683f9bdcd1bf29e9c11c29d10bbf44107ef952f7784c3c3b436edf4c7939780e7c4359c65429d261805680269422146e7ba3','Guadenicia','Guadenicia','mail@mail.com','villa','2',NULL,1,0,-2280,NULL,NULL),(5,'721596611','scrypt:32768:8:1$WfUOTvsiVi8s4KDm$365c04eafb408595296633afbf375f75ec8cca4f8b329a3208ab9baf01d5b3137f7231dcbf2e0cad94a3154f36c8277ca2236f594d82638ccc2d11081f3e62f9','hezekiel','ombima','mail@mail.com','osupuko','55',NULL,1,0,-200,NULL,NULL),(6,'716810254','scrypt:32768:8:1$7BgdQjhntjSAJPUD$d8a1616f5bfc16af739dfc7fc8f2ec78deb04cf2f8af3cdad27bd917f89b7a4bd407a375846a5eccd7296530bd26a1af63b10d879a7d20e37b7e6438624bfa96','Komi','Komi','mail@mail.com','phase 3','1',NULL,1,0,-2280,NULL,NULL),(7,'720652469','scrypt:32768:8:1$47Qia8lzte7Tkh5s$eaf28555c1c37e57f95e112ed63a3e3da77aaa29cd14939a7bdd698f0c85df8a3418c73c9eb6f3cea5617890ab1520a85d437d493c5d70a7236e1b672d64d9d3','Raphael','Koome','mail@mail.com','osupuko','52',NULL,1,0,0,NULL,NULL),(8,'722529258','scrypt:32768:8:1$P4uEITXXCIrTmQBC$cedbac7cfcb2aaee0da7198e0813a7739e5952fbdbf6d0a35b9691319083a31183b879914d7201080b9e941e3615d16cb348d56f12431a54536601e59f2c0b55','Hellen','marambii','mail@mail.com','osupuko','81',NULL,1,0,-330,NULL,NULL),(9,'722755547','scrypt:32768:8:1$WCTJlGG2Mg2oDyOb$8389f9bb7059a22239b87816d905e4cce3371b0b2601744d3d99aef8496385b3966a3000f1708daf98fa13e24b789c28376f8c6dd7d966fc0e2c71eb4ca170d2','christina','christina','mail@mail.com','osupuko','61',NULL,1,0,-2800,NULL,NULL),(10,'722578161','scrypt:32768:8:1$BDG3JTkimP2vcIfW$7b7ddd8110523b7708b5e6db785b093ec603fbc8f4c3397f909cdd2405b23984fad9f213dc938adb98024dc1d5401f6df813f26f2a979a3113300e13962612b0','susan','karongo','mail@mail.com','osupuko','19',NULL,1,0,-200,NULL,NULL),(11,'720200720','scrypt:32768:8:1$3vMyZiYI3m6H8VWz$24a82c647d3e2a78116f439b31901b2272113c7e4dea54a2f0c5fe3bb1a69c578ee4895df648d8036de238326ff3c86925ec510c2b6ae8e458124a4b87a14197','Eldiadia','mageni','mail@mail.com','osupuko','76',NULL,1,0,-200,NULL,NULL),(12,'701017754','scrypt:32768:8:1$ba7jkXeCZWTeF2FZ$1156844236f4e5c3d602c197363d3aa82fbbcfcc1ce9f8f5ec2cdd6a4a4176620ec79ca81e66d5b3a2a7ce5cc279261702673d7bd09dc6e46cef323117ebb0fc','emily','akuno','mail@mail.com','villa','5',NULL,1,0,-1760,NULL,NULL),(13,'790249941','scrypt:32768:8:1$UPhf5KW1LMvWWXeW$1743e1051267e4409df524bd547572a0e987fe697c80af7edbcd4c77ba697f890f3a50a25b6be30fbb9ba22bb3a44fb9d54417a37a3025a1950edd7881c19228','roman','hinga','mail@mail.com','osupuko','79',NULL,1,0,-330,NULL,NULL),(14,'721928657','scrypt:32768:8:1$jloRTiHROtoLy3ew$32b94af1d9e816a22bce881a3ec8b6421d5dd29692f561f4e1db32249169c00fb3f03cb821dfb79c8fb5e08239d0c80adbed71beb02366b96ee9481a838fa88c','Jeremiah','kariuki','mail@mail.com','osupuko','46',NULL,1,0,-200,NULL,NULL),(15,'723835905','scrypt:32768:8:1$SOFQv1xxqz5BroiZ$00c16da476f0f2a4e9644845b4f0e70b014c0afd946a38dacc31a1c3f4fe4715e42e89f156af6f6586455b405f34d4e0e04292afec1403a83f7746b3493f7438','jilo','guyo','mail@mail.com','osupuko','12',NULL,1,0,-1630,NULL,NULL),(16,'725297007','scrypt:32768:8:1$AJQXNsVsnmD14k3I$b90a9bd2aa8dd76e003ef55c4d9be303de8953d1a97b1fefff9f8ab26980c2f74f6812266fb1c810f98056ed9633c6107b08f327643daf75aa8337a283ee94c5','ruth','vulimu','mail@mail.com','osupuko','44',NULL,1,0,-980,NULL,NULL),(17,'714367580','scrypt:32768:8:1$d8PxtwDSmMmGOjPL$f91f6932da14554a50d3db2b2d7f422e49a9db114717940be39a8fe18b3a18d0eca684a74f1048fda91242c3ad1375e13f1bf3640fbdf40fc6a1720429441e16','Robert','leteipa','mail@mail.com','osupuko','21',NULL,1,0,-330,NULL,NULL),(18,'721458857','scrypt:32768:8:1$Tdi7TFjvRk3ZCw7P$12fba3caf57ae19dadb8e69560cfd8c0360a288e228ee13f411b560e1b6d28650be1fcb142a20cd00ddb25d8c48299d38a1dfe21e7fc2c56851b8f90cdf1400b','newton','njeru','mail@mail.com','osupuko','56',NULL,1,0,0,NULL,NULL),(19,'722643088','scrypt:32768:8:1$V0leKk5i19MJDtjB$51a97940ba86090aef0e2f2636e7dec71facfc68574875e6580515ef04d7b3114f4e759842985c5d4b33e51b21960619c56a8c8ac4ae59fa1ba9e67336a8feda','leah','kubai','mail@mail.com','osupuko','57',NULL,1,0,-200,NULL,NULL),(20,'723385885','scrypt:32768:8:1$vDBzQIqfKzOi95rV$4a419c04eb10f2d22cde445d712cef51b16c20f33ba7b0db3003bb69047e940f38cea3215640ccd6bad548e9f8c89de3c60d406b1152db778ff39c6b39ae9501','Trassey','emelda','trassyemelda@gmail.com','admin','1',NULL,1,1,0,'2024-02-28 00:51:56','2024-02-28 00:52:04'),(21,'722737482','scrypt:32768:8:1$cQawIMeJVGfLJHWR$9b5a284305388711b037a484b594004ad1b1168ca74727a286ed9c931c0e3c44321adb861d344f515f11e924dc469195086286b6f24bfe3531732b77cb800199','david','ngwirii','mail@mail.com','osupuko','6',NULL,1,0,-19960,NULL,NULL),(22,'720557389','scrypt:32768:8:1$hSPM5fKTF2fCaP0i$b98615db2a6adce373aa17f4fbecc73b87a4a9e05232ae0f3df967ee3ffc80f7741f833238931f4792abd555c554f0482dd30e77e9c0c9ac11d7e8167f628d1e','rose','osogo','mail@mail.com','osupuko','9',NULL,1,0,0,NULL,NULL),(23,'733643463','scrypt:32768:8:1$a0JshjF1iBXNnqQn$91aee15e80d239c4e715722a31fd11ddd6b2e263c34b37f924cde74b755ae8d9fae064d9e9c6ee40a616d82e0295c340f6915c5fedae648f2cf6fe2a71a33bd3','andrew','akoko','mail@mail.com','osupuko','11',NULL,1,0,-850,NULL,NULL),(24,'722262726','scrypt:32768:8:1$WABuoKMyto2pGuPX$81f116da504b7bc1c38180a64aa6005aa1ecd7280c2f888c6c05763f64157073ede23f556f17b6d0b540046ed67f89ce01968dcffb7c4e202a4b75cc428d6ab0','rodgers','mutai','mail@mail.com','osupuko','14',NULL,1,0,-1890,NULL,NULL),(25,'735547725','scrypt:32768:8:1$7SseTePyRIAiT22L$5b88226a924a17b5e29af15c369a21ee2315715664cbee6a86391f3137b471314d92e6e2f26f94dc0cbc4f6cc0d4475f23b4fda5d331d4e6b4f4e9ae1b0a9f87','cynthia','oliwa','mail@mail.com','osupuko','16',NULL,1,0,-200,NULL,NULL),(26,'722691767','scrypt:32768:8:1$zUsqIhCUfAOppr3r$3ac32be7e43d4e4e364906ccbff7a98136ce2c15eb87d6ed28753219520bb08fbacb1a016a11a05d345105b129a970286e07e0ca9d7742b74397dba0bf784187','simon','mwilu','mail@mail.com','osupuko','17',NULL,1,0,70,NULL,NULL),(27,'727341184','scrypt:32768:8:1$V5ga71Iq3clOyT8Y$cfc75925c8221f84064cf53eeb1d0d5635877b1770cd46d1ed2312e4681a94ad0c046f06f35e95caee9e194ed971ecc59c50a0def646f11700a59cd451ee58fd','evelyn','onamu','mail@mail.com','osupuko','20',NULL,1,0,-1110,NULL,NULL),(28,'720316694','scrypt:32768:8:1$IWXxXdEU94oPcf2g$2b8fc775703cc85c81bb7c1360f42b8eda3aff9b379d38547b394759d4480f856ce31d5bec4348dd857dcaeda6aacd59ffe0e10970926adde963680a9337d992','ibrahim','onyatta','mail@mail.com','osupuko','22',NULL,1,0,-1370,NULL,NULL),(29,'721748672','scrypt:32768:8:1$AVyba3IMMICyrgp7$8fe95e4f32deb1e0fcfc36dad80d681a2172237ba9b73bafd5b4db7e0943dc09c715ee6b041a57bb34e9046a4b9b69be05d79723ffde52756d7a87d152440a7d','kiragu','maina','mail@mail.com','osupuko','23',NULL,1,0,-330,NULL,NULL),(30,'747252791','scrypt:32768:8:1$8xT793rj6CMMsz3e$31321802fe3c3a61e2a71f02d39c92b57f3908c6edec520485641f53115ccbdca583a8cadc389aa6d8a61f595af73dee42435b20b8c13786eb759f659a79a2c4','joanne','joanne','mail@mail.com','osupuko','24',NULL,1,0,0,NULL,NULL),(31,'723344366','scrypt:32768:8:1$WA5QAJSRkbe2k4h8$1b023500f6f472c7db6f2bc26ea145a28e8b90a2dd683e6ef847fdf6c63bb116edd70639e86f4620637209e710f356f1c53c082bd5addaa283a8d25159f34109','Elizabeth','kamweru','mail@mail.com','osupuko','25',NULL,1,0,-2280,NULL,NULL),(32,'710591846','scrypt:32768:8:1$6zLl3rVZraTxscsy$c9b48fb1139049662566f47b3b23688b6fe7b6ae432664977fa07115a1852d7590e7d0beccfe90f82bc3a320b17e9a21a1c5782a80b95a9c09d76c7006964542','maria','maria','mail@mail.com','osupuko','27',NULL,1,0,-1500,NULL,NULL),(33,'722520413','scrypt:32768:8:1$45nfCBNB5cLUQ8AJ$e3ea95a6e01fac76b33efdb04a284b9e4ef482b4d1ef8ecf6b034be0d1856059f8a3e8bae9f9662adde63ab2c1abfc9ddf940a0933d1fe3959a974edcb47a870','george','ogwang','mail@mail.com','osupuko','48',NULL,1,0,0,NULL,NULL),(34,'715344355','scrypt:32768:8:1$Gdf5Qc7BUEqeeOw7$c37cf76a1fb13347e58e49dea086be8517805d8cbcd7abff7598d8372ceaad8c0721506b150126892e1f6c3fb3d4a3f5f0b5d40a7cf671ce2a386df742e58136','lillian','omosa','mail@mail.com','osupuko','49',NULL,1,0,0,NULL,NULL),(35,'772657163','scrypt:32768:8:1$IKo2VQcR2pshj6VO$a105cb15a2c8e121153dad6832d5317da35095d34cf4950e280bd5d01b731f49d7ccf36b34c51cfa2ce97288c8d34055a2a89fdac395f360388c04d3a7b0a339','stephen','ngwer (neville)','mail@mail.com','osupuko','50',NULL,1,0,0,NULL,NULL),(36,'721492288','scrypt:32768:8:1$XY8JSgZuo2iYKw1v$4f2638a7ae819c959e3ccbf6a9facd65e8091d30dfd8fbcc51e8e86349d44b5e34fd7a2b3de3b2a687ca711ee92c3741d967ec1822e939608119c54549a625d8','abanga','abanga','mail@mail.com','osupuko','51',NULL,1,0,-2410,NULL,NULL),(37,'726035617','scrypt:32768:8:1$5zUTVxUVIiVod9hi$ab83e19bc67d9e6a70245310c31e7972d5378423fd458be24f96aa340d4b79437106d4e7af774cb520054be83382448dd68076de4903bf2fe698e3b790437f45','brian','muturi','mail@mail.com','osupuko','54',NULL,1,0,-5270,NULL,NULL),(38,'722829979','scrypt:32768:8:1$pO47JF7h1OHTaEj0$db5f797ddf62cfd001cfb6f584022bd9c832058e37543d9430d0a5a3cbaed1b2e67dfa040c870370ff024b9780d52388f09c030ce27bb0642fc5d957bf0bf3d5','lydia','njuguna','mail@mail.com','osupuko','58',NULL,1,0,-1610,NULL,NULL),(39,'722306955','scrypt:32768:8:1$pzoE5XKRHDwQLttk$861032ce0e7bae4de08531f3f8e6feb00afcceb8087f497e7938673cf1b134b419b0933e2bb9198c24f546cd378d46e4d5fc213d4fe17c9c44a81c140ec99a39','geoffrey','malakweny','mail@mail.com','osupuko','59',NULL,1,0,0,NULL,NULL),(40,'711861244','scrypt:32768:8:1$tDEquIYh3F7prKak$b104225c57cdbb52d9b2619c1e0292e78ecce9a32108a684b9207096474e27d19474937b63c05319bfee32cd9c3b73727c17bc32e7a47ae7cfbc3b93058e4b60','steve','odinyo','mail@mail.com','osupuko','60',NULL,1,0,-200,NULL,NULL),(41,'722760456','scrypt:32768:8:1$SdA4BPCo35A5rlGG$1b2bc9a66f82160961e21ceead9c763d7e949c88b2cf8009dbf4f5bc1448dc00a0483950d6d4150d19bc8ab8e5b3efd94945708813eaf4e13933b908faf47acd','beatrice','okundi','mail@mail.com','osupuko','62',NULL,1,0,0,NULL,NULL),(42,'721806865','scrypt:32768:8:1$f9iFxrOvOTLAVPre$7fade628152f6f9e6e87da735168494bdb6b76075d98b5edc1b16f0646168a0aed88f8ce32096b94b73aec0e41967519c8b0ec8c94971fae941edb07c2a3d3f3','george','ambatta','mail@mail.com','osupuko','63',NULL,1,0,-200,NULL,NULL),(43,'722228173','scrypt:32768:8:1$AVedsK29IcnThHez$eebac12b3155b61afa6f498402d8f344e7a791a5873d79cf69904af9cc8f7f7cfd3dedeabdd70ef6feff87f5c81d175d9333211ee6f9ccea710169bf555cbb71','colette','aloo','mail@mail.com','osupuko','64',NULL,1,0,-200,NULL,NULL),(44,'729542619','scrypt:32768:8:1$7J9TVsHehmRck7f3$0660297a19bcfe55e4fb5e22d0f00bc1f2bf0e869e4f777e839a5d85ee8308c8d3f453f8462ee3023b372e52610a6c5305471397ab0a45b13cf3ca5a473471e7','irene','irene','mail@mail.com','osupuko','65',NULL,1,0,0,NULL,NULL),(45,'715694941','scrypt:32768:8:1$uWmisq1K4eZFzo0A$6678e8fcc9614f28edc66fac8fa8fbc96ae18c6141a539d98db9d67f0dfb232b7550c6bcecb4bf8c48a296698fd777ae4e0ec5492b0f513a599a2e0d90875828','ann','kamau','mail@mail.com','osupuko','66',NULL,1,0,-3060,NULL,NULL),(46,'723458372','scrypt:32768:8:1$KkX9oFaIZ5i3yMbx$20073ad336e37443b515ecc09f0515fac68cc3050786208e8928114036ea265b6314c94ad8d99921a5b478d3ce2e370cb630393a1e8133e41fa7848c903841c0','erick','korir','mail@mail.com','osupuko','67',NULL,1,0,-1890,NULL,NULL),(47,'712116927','scrypt:32768:8:1$j6JlhRYdsrGKBDnA$a1b6ee9a8fa2d2648430712e9e84571aeffea2ad920f1c1b3b5dfde5838353321562d0fe4a9b1638a08b4d88719c9646f9d8b9aca2fcb21c22566edb61841114','martha','nyambura','mail@mail.com','osupuko','72',NULL,1,0,0,NULL,NULL),(48,'722533909','scrypt:32768:8:1$6QJPYJbqVw4UOjPF$b7813489fff69d00f13606b666094bd071927c516eb791cb2a63747d2a9dd1eff14d3e8a935e1dbf5be0c7f11a9192608ae9b5b67b8393078add31598a864212','kankano','robert','mail@mail.com','osupuko','73',NULL,1,0,-200,NULL,NULL),(49,'722490315','scrypt:32768:8:1$UhDrQGbUnAvpXXHR$39178e80451a382d93c3f0867c2aa91a6533841a2fef7c1a2bb143ccd02615526059fab3e183a27f6e70297559535f9b8b1d08d98a3cf1a03d57c89f0ba6e1bc','catherine','james','mail@mail.com','osupuko','74',NULL,1,0,-2800,NULL,NULL),(50,'733707534','scrypt:32768:8:1$R0JapTBS4PEsAlMn$ac8e219fd140b19825bc24c3e058226777eb4d1f5d961ec3578c9575268225e201029175f3bd237c77dd75e8d7afb806b60a5db760bdd4a028e8394caca983a7','george','juma','mail@mail.com','osupuko','78',NULL,1,0,0,NULL,NULL),(51,'725629921','scrypt:32768:8:1$lRNCaNsxCrYVb9PU$e6cff0624f59e20abc5b87c1a87a755331ec84fdbb51e92f9ddeb77aaba626fe5f7ed6f5f08029c04ec8c6639191a996194426a85522c11e0cabdd5e24d7b129','jerusha','mwenda','mail@mail.com','osupuko','80',NULL,1,0,0,NULL,NULL),(52,'728586201','scrypt:32768:8:1$qpNEDe1Pj8iiPxC6$5a9854dea4e4a427a51d768a55fcd85e23222a5a83803719864407c684d0fbe58df4974d0dc7ec733ad178fdf360a4b2e36365a973f78760e849db8f2fb2ed7c','lukas','leboo','mail@mail.com','chui lane','1',NULL,1,0,-4620,NULL,NULL),(53,'721163455','scrypt:32768:8:1$bk8cz6JPKy767rjZ$2f458a89ebe4bea460bc82c17589b2efd1d456d97d2a68865fec383582f1b8e33ad9e9abe8545ad4d9eb98c3093111906ac38ada1bf1ba466ef8aa10a566b78e','daniel','mburu','mail@mail.com','chui lane','2',NULL,1,0,-850,NULL,NULL),(54,'712242701','scrypt:32768:8:1$ta03fwffIUZmuSFZ$8a7caeeabf43281e7a36212e26509d27cb6709ddec6b5c62c4c2b98e2ed747240326950d5ae04d7ead8a973f2b5d8a57cc866bd4c662d2763d6f66356ecd9fc4','ricahrd','wanjiku','mail@mail.com','phase 3','2',NULL,1,0,-200,NULL,NULL),(55,'700787335','scrypt:32768:8:1$TY7VQ0Nc12qDn33n$733d06e4afaa27bf0053cfbb63eb9834c08d8052be6f6d52dc23250053563cb2734e8a9080fca128cbec04096e9a8466f8e0e92fe9dbb04899eb4756c27956bc','grace','mburu','mail@mail.com','phase 3','3',NULL,1,0,-980,NULL,NULL),(56,'718543384','scrypt:32768:8:1$L7pjlPeY91HNNdtP$9d977d2604f6e86b0e3f701c378b35b659e19ff71c96110d680a5469793026f89b39c05ab0c31e1ff7de90cc8e54a372f4cdf9ba52bcc7730266876b3b90b651','newton','njeru','mail@mail.com','phase 3','4',NULL,1,0,-330,NULL,NULL),(57,'721805758','scrypt:32768:8:1$lVjw3Jp5BPpzUHuY$17159256e0a3d8b2b8395c971022dfa7038ec6373b251ea816200f92c0568ea00c9c0e8b539cf479896b97c6c4f029c6c0e6f4cbf233290f21e39ce6ad8f9f51','benjamin','okeyo','mail@mail.com','villa','3',NULL,1,0,-3450,NULL,NULL),(58,'721449538','scrypt:32768:8:1$vBpe8okbean46Yai$88d623ecd00c723ce0556a5b5c1967b63a933bdb1ae3f5f2ab73c4047ffc847a937dd5d321399211e49ae718b5dd51c979f0a5c8b4a68540a11b94107539565a','phyllis','barasa','mail@mail.com','villa','9',NULL,1,0,-1890,NULL,NULL),(59,'722529775','scrypt:32768:8:1$Oqmwn0GU4Wcwowg8$48f3b83d2b02b6d1afdf65b205da9fbcc78edfe3290353e7f56bb78501113749db8c9aa0c7d7dadd40ddb53360b4b5947acdef10db4504487bec791136e89596','truphosa','okwar','mail@mail.com','villa','10',NULL,1,0,-1110,NULL,NULL),(60,'722531443','scrypt:32768:8:1$xyNkpG5Eh1qu4vid$cb2c16d90b8bcc3f0f0fea6ea0cd411bb1e71c34f23fb111c4b388bcf38975083867815b1ce11b3e3e7dd3af95a3eca1afb6b15266844746cfd8cd34f0c2f595','michael','michael','mail@mail.com','osupuko','15',NULL,1,0,-4600,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-05 14:50:45
