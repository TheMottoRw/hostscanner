-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: localhost    Database: hostscanner
-- ------------------------------------------------------
-- Server version	8.0.29-0ubuntu0.22.04.2

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
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hostname` varchar(100) DEFAULT NULL,
  `current_ip` varchar(40) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `scan_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hosts`
--

LOCK TABLES `hosts` WRITE;
/*!40000 ALTER TABLE `hosts` DISABLE KEYS */;
INSERT INTO `hosts` VALUES (1,'ASUA-TECRA-Z50-A','192.168.43.120','Connected','2022-07-24 20:03:57'),(2,'_gateway','192.168.43.197','Connected','2022-07-24 20:26:28'),(3,'ASUA','192.168.43.175','Disconnected','2022-07-24 20:26:28'),(4,'LAB01','192.168.1.12','Disconnected','2022-04-03 13:34:10'),(5,'DESKTOP-P4J0FTC','192.168.1.14','Disconnected','2022-04-03 13:34:10'),(6,'Pixel-3a','192.168.1.15','Disconnected','2022-04-03 13:34:10'),(7,' _gateway','192.168.43.197','Disconnected','2022-07-24 20:25:11');
/*!40000 ALTER TABLE `hosts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_groups`
--

DROP TABLE IF EXISTS `ip_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ip_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) DEFAULT NULL,
  `first_ip` varchar(100) DEFAULT NULL,
  `last_ip` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_groups`
--

LOCK TABLES `ip_groups` WRITE;
/*!40000 ALTER TABLE `ip_groups` DISABLE KEYS */;
INSERT INTO `ip_groups` VALUES (1,'Floor 1','192.168.1.1','192.168.1.10','2022-05-28 11:31:35'),(2,'Floor Base','192.168.1.11','192.168.1.66','2022-05-28 11:34:32'),(3,'Floor 2','192.168.1.67','192.168.1.72','2022-05-28 12:01:13'),(4,'Rooftop','192.168.2.10','192.168.2.23','2022-07-01 12:09:04');
/*!40000 ALTER TABLE `ip_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_changes`
--

DROP TABLE IF EXISTS `status_changes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_changes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `host_id` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  `last_scan_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `status_changes_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `hosts` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_changes`
--

LOCK TABLES `status_changes` WRITE;
/*!40000 ALTER TABLE `status_changes` DISABLE KEYS */;
INSERT INTO `status_changes` VALUES (1,2,'Connected','Host reconnected','2022-03-20 12:12:39'),(2,1,'Connected','Host reconnected','2022-03-20 12:12:39'),(3,1,'Disconnected','Device disconnected from network','2022-03-20 12:12:39'),(4,2,'Disconnected','Device disconnected from network','2022-03-20 12:12:39'),(5,2,'Connected','Host reconnected but ip changed from 192.168.43.191 to 192.168.1.1','2022-03-20 12:12:39'),(6,3,'Connected','New host ASUA connected with ip:192.168.1.10','2022-03-20 12:12:39'),(7,1,'Connected','Host reconnected but ip changed from 192.168.43.120 to 192.168.1.12','2022-03-20 12:12:39'),(8,3,'Disconnected','Device disconnected from network','2022-03-20 12:12:39'),(9,3,'Connected','Host reconnected','2022-03-20 12:12:39'),(10,3,'Disconnected','Device disconnected from network','2022-04-02 14:13:54'),(11,3,'Connected','Host reconnected','2022-04-02 14:15:50'),(12,3,'Disconnected','Device disconnected from network','2022-04-02 14:32:07'),(13,3,'Connected','Host reconnected','2022-04-02 14:32:07'),(14,3,'Disconnected','Device disconnected from network','2022-04-02 14:57:13'),(15,3,'Disconnected','Device disconnected from network','2022-04-02 14:58:38'),(16,3,'Disconnected','Device disconnected from network','2022-04-02 15:01:45'),(17,4,'Connected','New host LAB01 connected with ip:192.168.1.12','2022-04-03 13:34:10'),(18,1,'Disconnected','Device disconnected from network','2022-04-03 13:34:10'),(19,5,'Connected','New host DESKTOP-P4J0FTC connected with ip:192.168.1.14','2022-04-03 13:34:10'),(20,6,'Connected','New host Pixel-3a connected with ip:192.168.1.15','2022-04-03 13:34:10'),(21,6,'Disconnected','Device disconnected from network','2022-04-03 13:34:10'),(22,1,'Connected','Host reconnected but ip changed from 192.168.1.12 to 192.168.43.120','2022-07-01 17:01:20'),(23,2,'Connected','Host reconnected but ip changed from 192.168.1.1 to 192.168.43.133','2022-07-01 17:01:20'),(24,4,'Disconnected','Device disconnected from network','2022-07-01 17:01:20'),(25,5,'Disconnected','Device disconnected from network','2022-07-01 17:01:20'),(26,2,'Connected','Host reconnected but ip changed from 192.168.43.133 to 192.168.43.197','2022-07-19 19:48:30'),(27,1,'Disconnected','Device disconnected from network','2022-07-19 19:48:30'),(28,2,'Disconnected','Device disconnected from network','2022-07-19 19:48:30'),(29,1,'Connected','Host reconnected','2022-07-19 19:55:46'),(30,1,'Disconnected','Device disconnected from network','2022-07-19 19:55:46'),(31,1,'Connected','Host reconnected','2022-07-19 19:56:59'),(32,2,'Connected','Host reconnected','2022-07-19 19:56:59'),(33,1,'Disconnected','Device disconnected from network','2022-07-19 19:56:59'),(34,2,'Disconnected','Device disconnected from network','2022-07-19 19:56:59'),(35,1,'Connected','Host reconnected','2022-07-19 19:59:02'),(36,2,'Connected','Host reconnected','2022-07-19 19:59:02'),(37,1,'Disconnected','Device disconnected from network','2022-07-19 19:59:02'),(38,2,'Disconnected','Device disconnected from network','2022-07-19 19:59:02'),(39,1,'Connected','Host reconnected','2022-07-19 20:01:40'),(40,2,'Connected','Host reconnected','2022-07-19 20:01:40'),(41,1,'Disconnected','Device disconnected from network','2022-07-19 20:01:40'),(42,2,'Disconnected','Device disconnected from network','2022-07-19 20:01:40'),(43,1,'Connected','Host reconnected','2022-07-19 20:04:01'),(44,2,'Connected','Host reconnected','2022-07-19 20:04:01'),(45,1,'Disconnected','Device disconnected from network','2022-07-19 20:04:01'),(46,2,'Disconnected','Device disconnected from network','2022-07-19 20:04:01'),(47,1,'Connected','Host reconnected','2022-07-19 20:09:04'),(48,2,'Connected','Host reconnected','2022-07-19 20:09:04'),(49,1,'Disconnected','Device disconnected from network','2022-07-19 20:09:04'),(50,2,'Disconnected','Device disconnected from network','2022-07-19 20:09:04'),(51,1,'Connected','Host reconnected','2022-07-19 20:09:04'),(52,2,'Connected','Host reconnected','2022-07-19 20:09:04'),(53,1,'Disconnected','Device disconnected from network','2022-07-19 20:09:04'),(54,2,'Disconnected','Device disconnected from network','2022-07-19 20:09:04'),(55,1,'Connected','Host reconnected','2022-07-19 20:09:04'),(56,2,'Connected','Host reconnected','2022-07-19 20:09:04'),(57,1,'Disconnected','Device disconnected from network','2022-07-24 16:57:12'),(58,2,'Disconnected','Device disconnected from network','2022-07-24 16:57:12'),(59,1,'Connected','Host reconnected','2022-07-24 17:04:04'),(60,2,'Connected','Host reconnected','2022-07-24 17:04:04'),(61,1,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(62,2,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(63,1,'Connected','Host reconnected','2022-07-24 17:04:04'),(64,1,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(65,1,'Connected','Host reconnected','2022-07-24 17:04:04'),(66,2,'Connected','Host reconnected','2022-07-24 17:04:04'),(67,1,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(68,2,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(69,1,'Connected','Host reconnected','2022-07-24 17:04:04'),(70,2,'Connected','Host reconnected','2022-07-24 17:04:04'),(71,1,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(72,2,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(73,1,'Connected','Host reconnected','2022-07-24 17:04:04'),(74,2,'Connected','Host reconnected','2022-07-24 17:04:04'),(75,1,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(76,2,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(77,1,'Connected','Host reconnected','2022-07-24 17:04:04'),(78,1,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(79,1,'Connected','Host reconnected','2022-07-24 17:04:04'),(80,2,'Connected','Host reconnected','2022-07-24 17:04:04'),(81,1,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(82,2,'Disconnected','Device disconnected from network','2022-07-24 17:04:04'),(83,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(84,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(85,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(86,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(87,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(88,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(89,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(90,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(91,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(92,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(93,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(94,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(95,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(96,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(97,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(98,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(99,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(100,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(101,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(102,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(103,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(104,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(105,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(106,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(107,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(108,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(109,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(110,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(111,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(112,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(113,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(114,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(115,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(116,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(117,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(118,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(119,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(120,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(121,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(122,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(123,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(124,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(125,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(126,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(127,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(128,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(129,1,'Connected','Host reconnected','2022-07-24 17:19:52'),(130,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(131,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(132,2,'Connected','Host reconnected','2022-07-24 17:19:52'),(133,1,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(134,2,'Disconnected','Device disconnected from network','2022-07-24 17:19:52'),(135,1,'Connected','Host reconnected','2022-07-24 20:03:42'),(136,2,'Connected','Host reconnected','2022-07-24 20:03:42'),(137,3,'Connected','Host reconnected but ip changed from 192.168.1.10 to 192.168.43.175','2022-07-24 20:25:11'),(138,7,'Connected','New host  _gateway connected with ip:192.168.43.197','2022-07-24 20:25:11'),(139,2,'Disconnected','Device disconnected from network','2022-07-24 20:25:11'),(140,3,'Disconnected','Device disconnected from network','2022-07-24 20:25:11'),(141,3,'Connected','Host reconnected','2022-07-24 20:25:11'),(142,2,'Connected','Host reconnected','2022-07-24 20:25:11'),(143,7,'Disconnected','Device disconnected from network','2022-07-24 20:25:11'),(144,3,'Disconnected','Device disconnected from network','2022-07-24 20:28:05');
/*!40000 ALTER TABLE `status_changes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `user_type` enum('Admin','Technician') DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_otp_needed` tinyint(1) DEFAULT NULL,
  `otp` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Ishimwe fabienne','mnzroger@gmail.com','Admin','$2b$12$AICzsqZAOcaG2ckO297YxupMqM2b5yxUzq5CNB17vdi.yF6q4PFp2',0,NULL,'2022-03-20 11:44:24'),(2,'Roger','hasua.mr@gmail.com',NULL,'$2b$12$nzhpWW4zso0frciRb7CnwODJ8o7tqBmkLTEnLX3wMjj0ysdbeoG42',0,NULL,'2022-05-28 10:33:15'),(3,'Roger','hasua.mr@gmail.fr','Technician','$2b$12$tCV3mig1uILqFdgb1o/zdOKil3OTTEfe9qXEPXoCI3QlrdNZotm3m',0,NULL,'2022-05-28 10:42:21'),(4,'Roger','hasua.mr@gmail.eu','Technician','$2b$12$p0jqNofhcoGh5NYyCTkF8uF2ITVT1IpjweKQgOC8egPHv13K2pmsO',0,NULL,'2022-05-28 10:43:17'),(5,'Roger','hasua.mr@gmail.ao','Technician','$2b$12$bZF38z1KlEX1UGWIk0NDhO589P2QTuFyB2VJHoPE/rDA0WToFAX5K',0,NULL,'2022-05-28 10:46:10'),(6,'Clement','cl@gmail.com','Technician','$2b$12$UVz3rWs6p7DfXjusxTzzyuiRJxs8j7.8yylwnYqoib38EirQj1qEq',0,NULL,'2022-05-28 10:46:10'),(7,'Archange','archange@gmal.com','Technician','$2b$12$tMEj/Sw9EhW9oSq1Y1vPJeAa4N1OaDNDMDy4rRXMHuI/EXAu.7UIu',0,NULL,'2022-05-28 10:46:10'),(8,'Tech','user@yopmail.com','Technician','$2b$12$wO9Qfw2TSxKKZ7FrDjt6y.dv50WmIGsIeoxvp1GBtVjrY.XrKHfv2',0,NULL,'2022-07-01 11:31:17');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `user_type` enum('Admin','Technician') DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_otp_needed` tinyint(1) DEFAULT NULL,
  `otp` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Ishimwe fabienne','','mnzroger@gmail.com','Admin','$2b$12$AICzsqZAOcaG2ckO297YxupMqM2b5yxUzq5CNB17vdi.yF6q4PFp2',0,NULL,'2022-03-20 11:44:24'),(3,'Roger','','hasua.mr@gmail.fr','Technician','$2b$12$tCV3mig1uILqFdgb1o/zdOKil3OTTEfe9qXEPXoCI3QlrdNZotm3m',0,NULL,'2022-05-28 10:42:21'),(4,'Roger','','hasua.mr@gmail.eu','Technician','$2b$12$p0jqNofhcoGh5NYyCTkF8uF2ITVT1IpjweKQgOC8egPHv13K2pmsO',0,NULL,'2022-05-28 10:43:17'),(5,'Roger','','hasua.mr@gmail.ao','Technician','$2b$12$bZF38z1KlEX1UGWIk0NDhO589P2QTuFyB2VJHoPE/rDA0WToFAX5K',0,NULL,'2022-05-28 10:46:10'),(6,'Clement','','cl@gmail.com','Technician','$2b$12$UVz3rWs6p7DfXjusxTzzyuiRJxs8j7.8yylwnYqoib38EirQj1qEq',0,NULL,'2022-05-28 10:46:10'),(7,'Archange','','archange@gmal.com','Technician','$2b$12$tMEj/Sw9EhW9oSq1Y1vPJeAa4N1OaDNDMDy4rRXMHuI/EXAu.7UIu',0,NULL,'2022-05-28 10:46:10'),(8,'Tech','','user@yopmail.com','Technician','$2b$12$wO9Qfw2TSxKKZ7FrDjt6y.dv50WmIGsIeoxvp1GBtVjrY.XrKHfv2',0,NULL,'2022-07-01 11:31:17'),(9,'Asua','0788349092','hasua@yopmail.com','Technician','$2b$12$0H0hx8bXWpZTp2VuZoXBTOJYl.SJWtvNE4ZwyMkYu4NcbKgd7UcVS',0,649628,'2022-07-19 21:29:40'),(11,'asua','0785453123','a@yopmail.com','Technician','$2b$12$B0gzo98bSpSRXnZwBm5YtO41hGwOJpCM4Sh90fwHyBOxIqp5nWgki',0,NULL,'2022-07-23 23:01:48');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-27 20:54:16
