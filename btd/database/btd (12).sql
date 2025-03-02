-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 19, 2025 at 09:33 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `btd`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL,
  `division_id` int(11) DEFAULT NULL,
  `district_id` int(11) DEFAULT NULL,
  `subdistrict_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `otp` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `email`, `password`, `role`, `division_id`, `district_id`, `subdistrict_id`, `name`, `otp`) VALUES
(1, 'pritom@gmail.com', 'pritom11', 'Police', NULL, 230004, NULL, 'pritom dam', ''),
(230004, 'singhosudip333@gmail.com', 'admin', 'District', 220001, 230004, NULL, 'Sylhet', '435829'),
(240001, 'h.sadi2002@gmail.com', 'admin', 'Sub district', 220001, 230004, 240001, 'Sylhet Sadar', ''),
(240002, 'sadi@gmail.com', 'admin', 'Sub district', 220001, 230004, 240002, 'South surma', ''),
(240003, 'polash@gmail.com', 'polash', 'Police', NULL, 230004, NULL, 'polash', ''),
(240004, 'nishatshirazy@gmail.com', 'nishat', 'Police', NULL, 230004, NULL, 'Nusrat zahan', ''),
(240005, 'damrahul09@gmail.com', 'pritom', 'Police', NULL, 230004, NULL, 'hamayath', '');

-- --------------------------------------------------------

--
-- Table structure for table `allowance_applicant`
--

CREATE TABLE `allowance_applicant` (
  `id` int(11) NOT NULL,
  `citizen_id` int(11) NOT NULL,
  `nid_number` varchar(17) NOT NULL,
  `name` varchar(255) NOT NULL,
  `father_name` varchar(255) NOT NULL,
  `mother_name` varchar(255) NOT NULL,
  `birth_date` datetime NOT NULL,
  `gender` varchar(10) NOT NULL,
  `present_address` text NOT NULL,
  `permanent_address` text NOT NULL,
  `mobile_number` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `application_date` datetime DEFAULT current_timestamp(),
  `subdistrict_id` int(11) NOT NULL,
  `documents` varchar(100) NOT NULL,
  `status` varchar(20) DEFAULT 'pending' CHECK (`status` in ('pending','approved','rejected'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `applicants`
--

CREATE TABLE `applicants` (
  `application_id` varchar(100) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `full_name` varchar(510) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `religion` varchar(255) NOT NULL,
  `birth_country` varchar(255) DEFAULT NULL,
  `birth_division_id` int(11) NOT NULL,
  `birth_district_id` int(11) NOT NULL,
  `birth_subdistrict_id` int(11) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `present_address` text NOT NULL,
  `permanent_address` text NOT NULL,
  `father_name` varchar(255) NOT NULL,
  `father_nid` varchar(20) NOT NULL,
  `mother_name` varchar(255) NOT NULL,
  `mother_nid` varchar(20) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `relationship` enum('mother','father','brother','sister') NOT NULL,
  `division_id` int(11) NOT NULL,
  `district_id` int(11) NOT NULL,
  `subdistrict_id` int(11) NOT NULL,
  `healthcare_id` int(11) NOT NULL,
  `application_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `user_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applicants`
--

INSERT INTO `applicants` (`application_id`, `first_name`, `last_name`, `full_name`, `gender`, `religion`, `birth_country`, `birth_division_id`, `birth_district_id`, `birth_subdistrict_id`, `birth_date`, `present_address`, `permanent_address`, `father_name`, `father_nid`, `mother_name`, `mother_nid`, `contact_number`, `relationship`, `division_id`, `district_id`, `subdistrict_id`, `healthcare_id`, `application_time`, `user_name`) VALUES
('BTD202409031056058082', 'aa', 'aa', 'aa aa', 'Male', 'Hindu', NULL, 220001, 230004, 240001, '2019-03-01', 'Sylhwt', 'Sylhwt', 'swxsx', '76744', 'fdgnd', '654654', '5365365', 'father', 220001, 230004, 240001, 8, '2024-09-03 08:56:05', NULL),
('BTD202409041256233026', 'Joytush', 'Das', 'Joytush Das', 'Other', 'Atheist', 'Bangladesh', 220001, 230004, 240002, '2020-02-01', 'sylhet', 'sylhet', 'Bipul Kanti Das', '12345345', 'Sobita Rani Das', '7654354', '2347543876', 'mother', 220001, 230004, 240001, 8, '2024-09-04 10:56:23', NULL),
('BTD202409042304163533', 'pritom', 'dam', 'pritom dam', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2002-01-22', 'sylhet,bangladesh', 'sylhet,bangladesh', 'Shoshanko Dam', '13453452', 'Gita rani dey', '78654574', '01301727106', 'mother', 220001, 230004, 240001, 9, '2024-09-04 21:04:16', NULL),
('BTD202502181907588939', 'pritom', 'dam', 'pritom dam', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'bangladesh', 'cgvhbjn', 'dfghjkhgf', '546789765', 'gfhgjkjhgf', '5467898765', '01301727106', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:07:58', 'nusrat'),
('BTD202502181914006312', 'sankarsan', 'das', 'sankarsan das', 'Female', 'h', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'bangladesh', 'bangladesh', 'gcf', '7654356767', 'xcfvgbhj', '234567654', '01301727106', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:14:00', 'nusrat'),
('BTD202502181918426068', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:18:42', 'nusrat'),
('BTD202502181921059394', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:21:05', 'nusrat'),
('BTD202502181923436681', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:23:43', 'nusrat'),
('BTD202502181926488220', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:26:48', 'nusrat'),
('BTD202502181928019487', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:28:01', 'nusrat'),
('BTD202502181928585999', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:28:58', 'nusrat'),
('BTD202502181929283470', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:29:28', 'nusrat'),
('BTD202502181937292493', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:37:29', 'nusrat'),
('BTD202502181937349776', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:37:34', 'nusrat'),
('BTD202502181939223387', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2024-02-02', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:39:22', 'nusrat'),
('BTD202502181941123798', 'sankarsan', 'das', 'sankarsan das', 'Male', 'Hindu', 'Bangladesh', 220001, 230004, 240001, '2025-02-18', 'sdfghjk', 'dfghjkl', 'dfghdgfh', '5467543456', 'vjfhgj', '5768765387654', '34567890876543', 'mother', 220001, 230004, 240001, 9, '2025-02-18 07:41:12', 'nusrat');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add admin', 6, 'add_admin'),
(22, 'Can change admin', 6, 'change_admin'),
(23, 'Can delete admin', 6, 'delete_admin'),
(24, 'Can view admin', 6, 'view_admin'),
(25, 'Can add applicant', 7, 'add_applicant'),
(26, 'Can change applicant', 7, 'change_applicant'),
(27, 'Can delete applicant', 7, 'delete_applicant'),
(28, 'Can view applicant', 7, 'view_applicant'),
(29, 'Can add baby reg', 8, 'add_babyreg'),
(30, 'Can change baby reg', 8, 'change_babyreg'),
(31, 'Can delete baby reg', 8, 'delete_babyreg'),
(32, 'Can view baby reg', 8, 'view_babyreg'),
(33, 'Can add citizen', 9, 'add_citizen'),
(34, 'Can change citizen', 9, 'change_citizen'),
(35, 'Can delete citizen', 9, 'delete_citizen'),
(36, 'Can view citizen', 9, 'view_citizen'),
(37, 'Can add district', 10, 'add_district'),
(38, 'Can change district', 10, 'change_district'),
(39, 'Can delete district', 10, 'delete_district'),
(40, 'Can view district', 10, 'view_district'),
(41, 'Can add division', 11, 'add_division'),
(42, 'Can change division', 11, 'change_division'),
(43, 'Can delete division', 11, 'delete_division'),
(44, 'Can view division', 11, 'view_division'),
(45, 'Can add nid verification', 12, 'add_nidverification'),
(46, 'Can change nid verification', 12, 'change_nidverification'),
(47, 'Can delete nid verification', 12, 'delete_nidverification'),
(48, 'Can view nid verification', 12, 'view_nidverification'),
(49, 'Can add vaccination schedule', 13, 'add_vaccinationschedule'),
(50, 'Can change vaccination schedule', 13, 'change_vaccinationschedule'),
(51, 'Can delete vaccination schedule', 13, 'delete_vaccinationschedule'),
(52, 'Can view vaccination schedule', 13, 'view_vaccinationschedule'),
(53, 'Can add vaccine', 14, 'add_vaccine'),
(54, 'Can change vaccine', 14, 'change_vaccine'),
(55, 'Can delete vaccine', 14, 'delete_vaccine'),
(56, 'Can view vaccine', 14, 'view_vaccine'),
(57, 'Can add vaccine status', 15, 'add_vaccinestatus'),
(58, 'Can change vaccine status', 15, 'change_vaccinestatus'),
(59, 'Can delete vaccine status', 15, 'delete_vaccinestatus'),
(60, 'Can view vaccine status', 15, 'view_vaccinestatus'),
(61, 'Can add volunteer', 16, 'add_volunteer'),
(62, 'Can change volunteer', 16, 'change_volunteer'),
(63, 'Can delete volunteer', 16, 'delete_volunteer'),
(64, 'Can view volunteer', 16, 'view_volunteer'),
(65, 'Can add subdistrict', 17, 'add_subdistrict'),
(66, 'Can change subdistrict', 17, 'change_subdistrict'),
(67, 'Can delete subdistrict', 17, 'delete_subdistrict'),
(68, 'Can view subdistrict', 17, 'view_subdistrict'),
(69, 'Can add passport applicant', 18, 'add_passportapplicant'),
(70, 'Can change passport applicant', 18, 'change_passportapplicant'),
(71, 'Can delete passport applicant', 18, 'delete_passportapplicant'),
(72, 'Can view passport applicant', 18, 'view_passportapplicant'),
(73, 'Can add nid applicant', 19, 'add_nidapplicant'),
(74, 'Can change nid applicant', 19, 'change_nidapplicant'),
(75, 'Can delete nid applicant', 19, 'delete_nidapplicant'),
(76, 'Can view nid applicant', 19, 'view_nidapplicant'),
(77, 'Can add healthcare', 20, 'add_healthcare'),
(78, 'Can change healthcare', 20, 'change_healthcare'),
(79, 'Can delete healthcare', 20, 'delete_healthcare'),
(80, 'Can view healthcare', 20, 'view_healthcare'),
(81, 'Can add passport verification', 21, 'add_passportverification'),
(82, 'Can change passport verification', 21, 'change_passportverification'),
(83, 'Can delete passport verification', 21, 'delete_passportverification'),
(84, 'Can view passport verification', 21, 'view_passportverification'),
(85, 'Can add monthly report', 22, 'add_monthlyreport'),
(86, 'Can change monthly report', 22, 'change_monthlyreport'),
(87, 'Can delete monthly report', 22, 'delete_monthlyreport'),
(88, 'Can view monthly report', 22, 'view_monthlyreport');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `baby_reg`
--

CREATE TABLE `baby_reg` (
  `reg_no` int(11) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `birth` varchar(20) DEFAULT NULL,
  `father_name` varchar(255) DEFAULT NULL,
  `father_nid` varchar(255) DEFAULT NULL,
  `mother_name` varchar(255) DEFAULT NULL,
  `mother_nid` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `vaccine_centre` varchar(255) DEFAULT NULL,
  `user_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `baby_reg`
--

INSERT INTO `baby_reg` (`reg_no`, `full_name`, `phone`, `birth`, `father_name`, `father_nid`, `mother_name`, `mother_nid`, `address`, `gender`, `vaccine_centre`, `user_name`) VALUES
(1, 'Pritom Dam Rahul', '01747467606', 'January 1, 2002', 'Shoshanko Dam', '101010', 'Gita Dey', '202020', 'Sylhet, Sylhet, Sylhet Sadar, hatkhola, 01', 'Female', NULL, ''),
(9, 'partho dam', '01747467607', 'January 1, 2002', 'Shoshanko Dam', '101010', 'Gita Dey', '202020', 'Sylhet, Sylhet, Sylhet Sadar, hatkhola, 01', 'Male', NULL, ''),
(10, 'sudip', '01655102001', 'January 1, 2000', 'shudharsan singho', '303030', 'Rajlakhshmi singha', '303030', 'Sylhet, Sylhet, Sylhet Sadar, hatkhola, 01', 'Male', NULL, ''),
(11, 'wdwe', '1222243', 'June 2, 2003', 'sfaf', '213423', 'sdfaaf', '2341', 'Sylhet, Sylhet, Sylhet Sadar, Kandigaon, 03', 'Male', NULL, 'h_sadi'),
(12, 'Pritom Dam Rahul', '2580', 'January 1, 2004', 'Shoshanko Dam', '12323243', 'Gita Dey', '1324313', 'Sylhet, Sylhet, Sylhet Sadar, hatkhola, 01', 'Male', 'Parkview Madical College', 'h_sadi');

-- --------------------------------------------------------

--
-- Table structure for table `citizen`
--

CREATE TABLE `citizen` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `father_name` varchar(255) DEFAULT NULL,
  `father_nid` varchar(255) DEFAULT NULL,
  `mother_name` varchar(255) DEFAULT NULL,
  `mother_nid` varchar(255) DEFAULT NULL,
  `present_division` varchar(255) DEFAULT NULL,
  `present_district` varchar(255) DEFAULT NULL,
  `present_upazila` varchar(255) DEFAULT NULL,
  `permanent_division` varchar(255) DEFAULT NULL,
  `permanent_district` varchar(255) DEFAULT NULL,
  `permanent_upazila` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `citizen`
--

INSERT INTO `citizen` (`id`, `name`, `email`, `username`, `password`, `birth_date`, `father_name`, `father_nid`, `mother_name`, `mother_nid`, `present_division`, `present_district`, `present_upazila`, `permanent_division`, `permanent_district`, `permanent_upazila`, `phone`) VALUES
(1, 'sadi', 'abc@gmail.com', 'sadi', '$2y$10$EJ2Nrcv7YRnTZL/eB7n9fex29P4jlJKSOiKOd8Ir7jUn.iLl7Aaa.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(2, 'pritom dam', 'joy@gmail.com', 'pritom', '$2y$10$01.IaF5ExG/YoQ18G6YE9eBULAIJSK7WPUu0T1rzbYpHQ57YwlBEO', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(3, 'Nusrat jahan', 'nusrat@gmail.com', 'nusrat', 'pbkdf2_sha256$600000$qSZLhQ5hlUqoDmv3uDg8pN$dtTf8US6PtO8M8UBMNb1JBw2la2kxabUg5F2sGjkJDE=', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(4, 'Sudip Singho', 'pritom@gmail.com', 'king23', 'pbkdf2_sha256$320000$rlWKzxdlKt9TAZ70WQJcTk$TK1ilNJNtc9thX4kIUioikq6XeUQ4ficiq9GRh+NJvo=', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `citizen_report`
--

CREATE TABLE `citizen_report` (
  `id` int(11) NOT NULL,
  `volunteer_id` int(11) NOT NULL,
  `healthcare_center_id` int(11) NOT NULL,
  `subdistrict_id` int(11) NOT NULL,
  `month` date NOT NULL,
  `births` int(11) NOT NULL,
  `vaccinations` int(11) NOT NULL,
  `deaths` int(11) NOT NULL,
  `submitted_at` datetime NOT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `citizen_report`
--

INSERT INTO `citizen_report` (`id`, `volunteer_id`, `healthcare_center_id`, `subdistrict_id`, `month`, `births`, `vaccinations`, `deaths`, `submitted_at`, `notes`) VALUES
(1, 9, 9, 240001, '2025-02-01', 435, 543, 54, '2025-02-08 10:13:41', 'sgdf');

-- --------------------------------------------------------

--
-- Table structure for table `districts`
--

CREATE TABLE `districts` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `division_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `districts`
--

INSERT INTO `districts` (`id`, `name`, `email`, `division_id`) VALUES
(230001, 'Moulivibazar', 'moulivibazar@btd.gov', 220001),
(230002, 'Sunamganj', 'sunamganj@btd.gov', 220001),
(230003, 'Habiganj', 'habiganj@btd.gov', 220001),
(230004, 'Sylhet', 'sylhet@btd.gov', 220001),
(230005, 'Mymensingh Sadar', 'mymensingh_sadar@btd.gov', 220002),
(230006, 'Netrokuna', 'netrokuna@btd.gov', 220002),
(230007, 'Jamalpur', 'jamalpur@btd.gov', 220002),
(230008, 'Sherpur', 'sherpur@btd.gov', 220002);

-- --------------------------------------------------------

--
-- Table structure for table `divisions`
--

CREATE TABLE `divisions` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `divisions`
--

INSERT INTO `divisions` (`id`, `name`, `email`) VALUES
(220001, 'Sylhet', 'sylhet@btd.gov'),
(220002, 'Mymensingh', 'mymensingh@btd.gov');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(6, 'citizen', 'admin'),
(7, 'citizen', 'applicant'),
(8, 'citizen', 'babyreg'),
(9, 'citizen', 'citizen'),
(10, 'citizen', 'district'),
(11, 'citizen', 'division'),
(20, 'citizen', 'healthcare'),
(22, 'citizen', 'monthlyreport'),
(19, 'citizen', 'nidapplicant'),
(12, 'citizen', 'nidverification'),
(18, 'citizen', 'passportapplicant'),
(21, 'citizen', 'passportverification'),
(17, 'citizen', 'subdistrict'),
(13, 'citizen', 'vaccinationschedule'),
(14, 'citizen', 'vaccine'),
(15, 'citizen', 'vaccinestatus'),
(16, 'citizen', 'volunteer'),
(5, 'contenttypes', 'contenttype');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-01-27 09:17:34.589139'),
(2, 'auth', '0001_initial', '2025-01-27 09:17:35.113405'),
(3, 'admin', '0001_initial', '2025-01-27 09:17:35.266696'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-01-27 09:17:35.280650'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-01-27 09:17:35.289630'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-01-27 09:17:35.348134'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-01-27 09:17:35.416950'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-01-27 09:17:35.439475'),
(9, 'auth', '0004_alter_user_username_opts', '2025-01-27 09:17:35.450671'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-01-27 09:17:35.522826'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-01-27 09:17:35.532379'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-01-27 09:17:35.548056'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-01-27 09:17:35.573560'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-01-27 09:17:35.588603'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-01-27 09:17:35.615466'),
(16, 'auth', '0011_update_proxy_permissions', '2025-01-27 09:17:35.634733'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-01-27 09:17:35.671395'),
(19, 'citizen', '0001_initial', '2025-01-27 14:54:04.946065');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1p9ts37w4234pbgh9qwpngjs4i72mxbx', '.eJxVjssOgjAQRX-FdE0MChtZ6cqVKz7ADO3ETtKH6YNEjf8uRUC6nHtvzpw3G6yKJiC6GwnWHstNYEAja9kDXJCWbRvUQGqtTvd07rjV2UgiqCA5uAS5ni-F9RoMFRoFcVDZ1sdekA-OeJg8Dk1VVfuS_RmLHqdALzTTWZcsenSzp4neQRixIDSZDPNL5l33VBJD0YEAt66dVVMX-2IRGbvcqR5hTQoH8mTnD4f04fMFYj5wQw:1tkqho:zQ01mB3fmWD7g3fklwYS-ul2AifgUDBMZASpcHFU1VY', '2025-03-05 20:30:04.452276'),
('9a6dmyy8ntjnznip4fs68m0jhwc9qygg', 'eyJjaXRpemVuX2lkIjozLCJ1c2VybmFtZSI6Im51c3JhdCJ9:1thUiF:hJ0CVZEEuWenp40_mtguzH2mGMj-1ikJJ7660Fq22oA', '2025-02-24 14:24:39.557950'),
('d50yt1a48iyt8k06x8v0jtxnwta6li1l', '.eJyrVkpMyc3Mi89MUbIyMjYwMDDRgYrkJeamKlkpBVfmZKSWKMFEi_JzQKIumcUlRZnJIPEUKBPFiJTMsszizHyouUZAQcNaAFVdIlg:1tcWMu:RqZf-hgX0dxw2JonaJelAhgmmK-0Uf_XOG2HD979oSE', '2025-02-10 21:10:04.841281'),
('p1lxrfzqhb41u8hn7pbzwh7pbm7lgz9g', '.eJyrVkrOLMmsSs2Lz0xRsjLRUSotTi3KS8xNVbJSys7MSzcyVtJRSkzJzYQoMDI2MDAwgYlA1QVX5mSklsDVFeXngERdMotLijKTQeIpUCaKESmZZZnFmflQc42Agoa1APLELbQ:1tdHNA:thaEBYUjQA8HsPROQDZgFv55fHTmBPtlHDCVAlw6jTI', '2025-02-12 23:21:28.994732'),
('stbe6e1d83zqg4fc2atdsar7kcakpj73', '.eJyrVkrOLMmsSs2Lz0xRsjLWUSotTi3KS8xNVbJSyistLkosUdJRSkzJzYQoMDI2MDAwgYlA1QVX5mSkItQV5eeARF0yi0uKMpNB4ilQJooRKZllmcWZ-VBzjYCChrUAL8kuQg:1tdHaq:zTsym3SaNlMs3fWJQeLJgqkgTJnDDWKcEAJvLPECfZk', '2025-02-12 23:35:36.673420');

-- --------------------------------------------------------

--
-- Table structure for table `healthcare`
--

CREATE TABLE `healthcare` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `subdistrict_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `healthcare`
--

INSERT INTO `healthcare` (`id`, `name`, `subdistrict_id`) VALUES
(8, 'parkview medical college', 240001),
(9, 'MAG osmani medical', 240001),
(12, 'Women\'s medical college', 240001),
(14, 'Al-haramain medical', 240001),
(15, 'north east medical college', 240001),
(16, 'Ibne Sina Hospital', 240001);

-- --------------------------------------------------------

--
-- Table structure for table `nid_applicant`
--

CREATE TABLE `nid_applicant` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `father_name` varchar(255) NOT NULL,
  `father_nid` varchar(50) DEFAULT NULL,
  `mother_name` varchar(255) NOT NULL,
  `mother_nid` varchar(50) DEFAULT NULL,
  `husband_name` varchar(255) DEFAULT NULL,
  `wife_name` varchar(255) DEFAULT NULL,
  `birth_id` varchar(50) NOT NULL,
  `birth_date` date NOT NULL,
  `birth_place` varchar(255) NOT NULL,
  `gender` varchar(10) DEFAULT NULL CHECK (`gender` in ('Male','Female','Other')),
  `marital_status` varchar(15) DEFAULT NULL CHECK (`marital_status` in ('Married','Unmarried','Widowed','Divorced')),
  `occupation` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL CHECK (`blood_group` in ('A+','A-','B+','B-','AB+','AB-','O+','O-')),
  `subdistrict_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'pending',
  `academic_certificate` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nid_applicant`
--

INSERT INTO `nid_applicant` (`id`, `name`, `father_name`, `father_nid`, `mother_name`, `mother_nid`, `husband_name`, `wife_name`, `birth_id`, `birth_date`, `birth_place`, `gender`, `marital_status`, `occupation`, `email`, `blood_group`, `subdistrict_id`, `status`, `academic_certificate`, `created_at`, `updated_at`) VALUES
(1, 'pritom', 'shoshanko', '5646541654', 'gita rani dey', '4684848485878', '', '', '15454152415', '1999-12-26', 'sylhet', 'Male', 'Unmarried', 'student ', 'singhosudip333@gmail.com', 'A+', 240001, 'approved', 'academic_certificates/Simulation_main.pdf', NULL, '2025-01-28 22:25:03.352190'),
(2, 'Alice Smith', 'Michael Smith', '2345678901', 'Laura Smith', '1987654321', NULL, NULL, 'BID234567', '1910-05-15', 'City B', 'Female', 'Married', 'Doctor', 'singhosudip333@gmail.com', 'B+', 240001, 'approved', '', '2023-10-02 11:00:00.000000', '2025-01-29 21:52:40.417511'),
(3, 'Bob Johnson', 'David Johnson', '3456789012', 'Emma Johnson', '2987654321', NULL, NULL, 'BID345678', '1978-08-20', 'City C', 'Male', 'Married', 'Teacher', 'bob.johnson@example.com', 'O+', 240001, 'rejected', NULL, '2023-10-03 12:00:00.000000', '2023-10-03 12:00:00.000000'),
(4, 'Carol White', 'James White', '4567890123', 'Olivia White', '3987654321', NULL, NULL, 'BID456789', '1992-12-25', 'City D', 'Female', 'Married', 'Nurse', 'carol.white@example.com', 'AB+', 240001, 'pending', NULL, '2023-10-04 13:00:00.000000', '2023-10-04 13:00:00.000000'),
(5, 'Test User 1', 'Father 1', NULL, 'Mother 1', NULL, NULL, NULL, '20240001', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test1@example.com', 'A+', 240001, 'approved', NULL, '2025-01-15 00:51:40.000000', NULL),
(6, 'Test User 2', 'Father 2', NULL, 'Mother 2', NULL, NULL, NULL, '20240002', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test2@example.com', 'A+', 240001, 'rejected', NULL, '2025-01-16 00:51:40.000000', NULL),
(7, 'Test User 3', 'Father 3', NULL, 'Mother 3', NULL, NULL, NULL, '20240003', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test3@example.com', 'A+', 240001, 'rejected', NULL, '2025-01-15 00:51:40.000000', NULL),
(8, 'Test User 4', 'Father 4', NULL, 'Mother 4', NULL, NULL, NULL, '20240004', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test4@example.com', 'A+', 240001, 'approved', NULL, '2025-01-15 00:51:40.000000', NULL),
(9, 'Test User 5', 'Father 5', NULL, 'Mother 5', NULL, NULL, NULL, '20240005', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test5@example.com', 'A+', 240001, 'approved', NULL, '2025-01-14 00:51:40.000000', NULL),
(10, 'Test User 11', 'Father 11', NULL, 'Mother 11', NULL, NULL, NULL, '20240011', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test11@example.com', 'A+', 240001, 'pending', NULL, '2025-01-11 00:51:40.000000', NULL),
(11, 'Test User 12', 'Father 12', NULL, 'Mother 12', NULL, NULL, NULL, '20240012', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test12@example.com', 'A+', 240001, 'rejected', NULL, '2025-01-14 00:51:40.000000', NULL),
(12, 'Test User 13', 'Father 13', NULL, 'Mother 13', NULL, NULL, NULL, '20240013', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test13@example.com', 'A+', 240001, 'approved', NULL, '2025-01-16 00:51:40.000000', NULL),
(13, 'Test User 14', 'Father 14', NULL, 'Mother 14', NULL, NULL, NULL, '20240014', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test14@example.com', 'A+', 240001, 'pending', NULL, '2025-01-14 00:51:40.000000', NULL),
(14, 'Test User 15', 'Father 15', NULL, 'Mother 15', NULL, NULL, NULL, '20240015', '1990-01-01', 'Dhaka', 'Male', 'Unmarried', 'Service', 'test15@example.com', 'A+', 240001, 'pending', NULL, '2025-01-16 00:51:40.000000', NULL),
(20, 'Week User 1', 'Father 1', NULL, 'Mother 1', NULL, NULL, NULL, '20240001', '1995-01-01', 'Dhaka', 'Female', 'Married', 'Business', 'week1@example.com', 'B+', 240001, 'approved', NULL, '2025-02-01 00:51:40.000000', NULL),
(21, 'Week User 2', 'Father 2', NULL, 'Mother 2', NULL, NULL, NULL, '20240002', '1995-01-01', 'Dhaka', 'Female', 'Married', 'Business', 'week2@example.com', 'B+', 240001, 'approved', NULL, '2025-02-03 00:51:40.000000', NULL),
(22, 'Week User 3', 'Father 3', NULL, 'Mother 3', NULL, NULL, NULL, '20240003', '1995-01-01', 'Dhaka', 'Female', 'Married', 'Business', 'week3@example.com', 'B+', 240001, 'approved', NULL, '2025-02-04 00:51:40.000000', NULL),
(23, 'Week User 4', 'Father 4', NULL, 'Mother 4', NULL, NULL, NULL, '20240004', '1995-01-01', 'Dhaka', 'Female', 'Married', 'Business', 'week4@example.com', 'B+', 240001, 'pending', NULL, '2025-01-30 00:51:40.000000', NULL),
(24, 'Week User 5', 'Father 5', NULL, 'Mother 5', NULL, NULL, NULL, '20240005', '1995-01-01', 'Dhaka', 'Female', 'Married', 'Business', 'week5@example.com', 'B+', 240001, 'pending', NULL, '2025-02-03 00:51:40.000000', NULL),
(27, 'Recent User 1', 'Father 1', NULL, 'Mother 1', NULL, NULL, NULL, '20240001', '2000-01-01', 'Dhaka', 'Male', 'Unmarried', 'Student', 'recent1@example.com', 'O+', 240001, 'approved', NULL, '2025-02-04 00:51:40.000000', NULL),
(28, 'Recent User 2', 'Father 2', NULL, 'Mother 2', NULL, NULL, NULL, '20240002', '2000-01-01', 'Dhaka', 'Male', 'Unmarried', 'Student', 'recent2@example.com', 'O+', 240001, 'rejected', NULL, '2025-02-04 00:51:40.000000', NULL),
(29, 'Recent User 3', 'Father 3', NULL, 'Mother 3', NULL, NULL, NULL, '20240003', '2000-01-01', 'Dhaka', 'Male', 'Unmarried', 'Student', 'recent3@example.com', 'O+', 240001, 'rejected', NULL, '2025-02-04 00:51:40.000000', NULL),
(30, 'Recent User 4', 'Father 4', NULL, 'Mother 4', NULL, NULL, NULL, '20240004', '2000-01-01', 'Dhaka', 'Male', 'Unmarried', 'Student', 'recent4@example.com', 'O+', 240001, 'approved', '', '2025-02-04 00:51:40.000000', '2025-02-08 15:53:31.768309'),
(31, 'Recent User 5', 'Father 5', NULL, 'Mother 5', NULL, NULL, NULL, '20240005', '2000-01-01', 'Dhaka', 'Male', 'Unmarried', 'Student', 'recent5@example.com', 'O+', 240001, 'approved', NULL, '2025-02-04 00:51:40.000000', NULL),
(32, 'Nusrat jahan', 'get', '6626699', 'fghj,h', '8802888', '', '', '1345654321``', '2000-01-11', 'sylhet', 'Female', 'Married', 'student ', 'pritomdam18@gmail.com', 'A+', 240001, 'pending', 'academic_certificates/phase_3.pdf', '2025-02-18 07:50:27.375913', '2025-02-18 07:50:27.386302');

-- --------------------------------------------------------

--
-- Table structure for table `nid_verification`
--

CREATE TABLE `nid_verification` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` varchar(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `father_name` varchar(255) NOT NULL,
  `mother_name` varchar(255) NOT NULL,
  `birth_date` date NOT NULL,
  `blood_group` varchar(5) NOT NULL,
  `verification_date` date NOT NULL,
  `fingerprint_status` varchar(10) DEFAULT 'pending' CHECK (`fingerprint_status` in ('pending','completed')),
  `face_status` varchar(10) NOT NULL DEFAULT 'pending',
  `face_photo` varchar(255) DEFAULT NULL,
  `nid_number` varchar(17) DEFAULT NULL,
  `verification_status` varchar(10) DEFAULT 'pending' CHECK (`verification_status` in ('pending','verified')),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nid_verification`
--

INSERT INTO `nid_verification` (`id`, `user_id`, `name`, `father_name`, `mother_name`, `birth_date`, `blood_group`, `verification_date`, `fingerprint_status`, `face_status`, `face_photo`, `nid_number`, `verification_status`, `created_at`) VALUES
(1, 'BTD00000001', 'pritom', 'shoshanko', 'gita rani dey', '1999-12-26', 'A+', '2025-01-30', 'completed', 'completed', '', '1999122600000001', 'verified', '2025-01-28 15:17:07'),
(3, 'BTD00000002', 'Alice Smith', 'Michael Smith', 'Laura Smith', '1910-05-15', 'B+', '2025-01-31', 'completed', 'completed', '', '1985051500000001', 'verified', '2025-01-29 15:52:40'),
(4, 'BTD00000030', 'Recent User 4', 'Father 4', 'Mother 4', '2000-01-01', 'O+', '2025-02-09', 'completed', 'completed', 'media/nid_faces/face_kf9st9R.jpg', '2000010100000001', 'verified', '2025-02-08 09:53:31');

-- --------------------------------------------------------

--
-- Table structure for table `passport_applicant`
--

CREATE TABLE `passport_applicant` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name_en` varchar(255) NOT NULL,
  `name_bn` varchar(255) NOT NULL,
  `father_name` varchar(255) NOT NULL,
  `father_nationality` varchar(100) NOT NULL,
  `mother_name` varchar(255) NOT NULL,
  `mother_nationality` varchar(100) NOT NULL,
  `spouse_name` varchar(255) DEFAULT NULL,
  `spouse_nationality` varchar(100) DEFAULT NULL,
  `nid_number` varchar(20) NOT NULL,
  `birth_certificate_number` varchar(20) NOT NULL,
  `birth_date` date NOT NULL,
  `birth_place` varchar(255) NOT NULL,
  `birth_country` varchar(100) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `marital_status` varchar(10) NOT NULL,
  `profession` varchar(100) NOT NULL,
  `present_address` text NOT NULL,
  `present_district_id` int(11) DEFAULT NULL,
  `present_subdistrict_id` int(11) DEFAULT NULL,
  `permanent_address` text NOT NULL,
  `permanent_district_id` int(11) DEFAULT NULL,
  `permanent_subdistrict_id` int(11) DEFAULT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `passport_type` varchar(10) DEFAULT NULL CHECK (`passport_type` in ('regular','official','diplomatic')),
  `page_type` varchar(2) NOT NULL,
  `delivery_type` varchar(10) DEFAULT NULL CHECK (`delivery_type` in ('regular','urgent')),
  `application_status` varchar(30) DEFAULT 'pending',
  `tracking_number` varchar(20) DEFAULT NULL,
  `old_passport_number` varchar(20) DEFAULT NULL,
  `old_passport_issue_date` date DEFAULT NULL,
  `old_passport_expiry_date` date DEFAULT NULL,
  `nid_scan` varchar(255) NOT NULL,
  `birth_certificate_scan` varchar(255) NOT NULL,
  `old_passport_scan` varchar(255) DEFAULT NULL,
  `payment_amount` decimal(10,2) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT 'pending',
  `payment_date` timestamp NULL DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `police_verification_status` varchar(20) DEFAULT 'pending',
  `police_verification_date` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `citizen_id` int(11) DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `card_number` varchar(20) DEFAULT NULL,
  `bkash_number` varchar(15) DEFAULT NULL,
  `police_station` varchar(255) DEFAULT NULL,
  `police_officer` varchar(255) DEFAULT NULL,
  `criminal_records_found` tinyint(1) DEFAULT 0,
  `address_verified` tinyint(1) DEFAULT 0,
  `police_comments` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `passport_applicant`
--

INSERT INTO `passport_applicant` (`id`, `name_en`, `name_bn`, `father_name`, `father_nationality`, `mother_name`, `mother_nationality`, `spouse_name`, `spouse_nationality`, `nid_number`, `birth_certificate_number`, `birth_date`, `birth_place`, `birth_country`, `gender`, `marital_status`, `profession`, `present_address`, `present_district_id`, `present_subdistrict_id`, `permanent_address`, `permanent_district_id`, `permanent_subdistrict_id`, `phone`, `email`, `passport_type`, `page_type`, `delivery_type`, `application_status`, `tracking_number`, `old_passport_number`, `old_passport_issue_date`, `old_passport_expiry_date`, `nid_scan`, `birth_certificate_scan`, `old_passport_scan`, `payment_amount`, `payment_status`, `payment_date`, `transaction_id`, `police_verification_status`, `police_verification_date`, `created_at`, `updated_at`, `citizen_id`, `payment_method`, `card_number`, `bkash_number`, `police_station`, `police_officer`, `criminal_records_found`, `address_verified`, `police_comments`) VALUES
(4, 'pritom dam', 'pritom dam', 'shoshanko', 'Bangladeshi', 'gita rani dey', 'Bangladeshi', '', '', '3216574561567465', '31657987864', '1999-05-11', 'sylhet', 'Bangladesh', 'male', 'single', 'student', 'bangladesh', 230004, 240001, 'bangladesh', 230004, 240001, '01301727106', 'singhosudip333@gmail.com', 'regular', '48', 'regular', 'verfied', 'BTD00000001', NULL, NULL, NULL, 'Simulation_main.pdf', 'Simulation_main.pdf', NULL, 5500.00, 'paid', '2025-01-29 02:38:24', 'TRX2025012908380KIC0W', 'verified', NULL, '2025-01-29 02:36:47', '2025-01-29 23:25:32', 3, 'bkash', NULL, '01726576876', 'dhy', 'dfhyrt', 0, 1, NULL),
(5, 'sdfgsdf', 'sdfsdfsd', 'sdfsdfsdf', 'sdfsdf', 'sdfsdfsdf', 'sdfsdfsdf', 'sdfsdfsdf', 'sdfsdf', '343434343434', '434343434434', '2014-03-04', 'sfsfsdf', 'dfgsdfsdf', 'male', 'divorced', 'sdfsfsdf', 'sdfsdfsdfd', 230004, 240002, 'Mirjanjangal, 15/1', 230004, 240002, '08131075999', 'singhosudip333@gmail.com', 'regular', '48', 'regular', 'pending', 'BTD00000002', NULL, NULL, NULL, 'Lucture-1.pdf', 'Lecture-8.pdf', 'Lecture-7.pdf', NULL, NULL, NULL, 'TRX2025012922147AILN8', 'pending', NULL, '2025-01-29 16:11:04', '2025-02-09 16:04:57', 4, NULL, NULL, NULL, NULL, NULL, 0, 0, NULL),
(6, 'partho dam ', 'partho', 'shoshanko', 'Bangladeshi', 'gita rani dey', 'Bangladeshi', '', '', '987654321', '2000010100000001', '2021-10-09', 'sylhet', 'Bangladesh', 'male', 'single', 'student', 'bangladesh', 230004, 240001, 'bangladesh', 230004, 240001, '01301727106', 'pritomdam18@gmail.com', 'regular', '48', 'urgent', 'pending', 'BTD00000003', NULL, NULL, NULL, 'this is made by pritom.pdf', 'Birth Certificate11.pdf', NULL, 5500.00, 'paid', '2025-02-09 10:19:22', NULL, 'verified', '2025-02-09 10:20:00', '2025-02-09 10:17:28', '2025-02-10 14:16:57', 3, 'bkash', NULL, NULL, 'kotwali', 'hfbdf', 0, 1, 'ytfrt'),
(8, 'sadi', 'sadi', 'gfjo', 'Bangladeshi', 'wsrgtf', 'Bangladeshi', '', '', '8648623874823', '232354234523', '1995-09-18', 'sylhet', 'Bangladesh', 'male', 'single', 'student', 'bangladesh', 230004, 240001, 'bangladesh', 230004, 240001, '01301727106', 'pritomdam18@gmail.com', 'regular', '48', 'regular', 'pending', 'BTD00000004', NULL, NULL, NULL, 'BUS Time - Copy - Copy (2) - Copy.pdf', 'django roadmap.pdf', NULL, 5500.00, 'paid', '2025-02-18 16:03:53', 'rfgjhfg4141', 'verified', '2025-02-19 01:46:43', '2025-02-18 16:00:43', '2025-02-19 08:03:57', 3, 'bkash', NULL, '01301727106', 'kotwali', 'pritom dam', 0, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `passport_verification`
--

CREATE TABLE `passport_verification` (
  `id` int(11) NOT NULL,
  `application_id` bigint(20) UNSIGNED DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `fingerprint_status` enum('pending','completed') DEFAULT 'pending',
  `face_status` enum('pending','completed') DEFAULT 'pending',
  `face_photo` varchar(255) DEFAULT NULL,
  `verification_status` enum('pending','verified') DEFAULT 'pending',
  `verification_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `print_status` varchar(10) NOT NULL DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `passport_verification`
--

INSERT INTO `passport_verification` (`id`, `application_id`, `passport_number`, `fingerprint_status`, `face_status`, `face_photo`, `verification_status`, `verification_date`, `created_at`, `updated_at`, `print_status`) VALUES
(4, 4, 'BD199905000001', 'completed', 'completed', NULL, 'verified', '2025-01-29', '2025-01-29 17:27:04', '2025-01-29 17:27:14', 'pending'),
(5, 6, 'BD202110000001', 'completed', 'completed', 'passport_faces/face.jpg', 'verified', '2025-02-10', '2025-02-09 10:22:43', '2025-02-10 08:03:41', 'pending'),
(7, 8, 'BD199509000001', 'completed', 'completed', 'passport_faces/face_bv1uuZA.jpg', 'verified', '2025-02-19', '2025-02-19 03:15:19', '2025-02-19 06:44:18', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `subdistricts`
--

CREATE TABLE `subdistricts` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `district_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subdistricts`
--

INSERT INTO `subdistricts` (`id`, `name`, `email`, `district_id`) VALUES
(240001, 'Syllhet Sadar', 'sylhet_sadar@btd.gov', 230004),
(240002, 'South surma', 'surma@gmail.com', 230004);

-- --------------------------------------------------------

--
-- Table structure for table `vaccination_schedule`
--

CREATE TABLE `vaccination_schedule` (
  `id` int(11) NOT NULL,
  `application_id` varchar(100) NOT NULL,
  `vaccine_id` int(11) NOT NULL,
  `dose_number` int(11) NOT NULL,
  `scheduled_date` varchar(100) NOT NULL,
  `status` enum('Pending','Done') DEFAULT 'Pending',
  `healthcare_id` int(11) NOT NULL,
  `volunteer_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vaccination_schedule`
--

INSERT INTO `vaccination_schedule` (`id`, `application_id`, `vaccine_id`, `dose_number`, `scheduled_date`, `status`, `healthcare_id`, `volunteer_id`) VALUES
(208, 'BTD202409041256233026', 1, 1, '2020-02-02', 'Done', 8, NULL),
(209, 'BTD202409041256233026', 3, 1, '2020-03-14', 'Done', 8, NULL),
(210, 'BTD202409041256233026', 3, 2, '2020-04-11', 'Done', 8, NULL),
(211, 'BTD202409041256233026', 3, 3, '2020-05-09', 'Done', 8, NULL),
(212, 'BTD202409041256233026', 4, 1, '2020-03-14', 'Done', 8, NULL),
(213, 'BTD202409041256233026', 4, 2, '2020-04-11', 'Done', 8, NULL),
(214, 'BTD202409041256233026', 4, 3, '2020-05-09', 'Done', 8, NULL),
(215, 'BTD202409041256233026', 5, 1, '2020-03-14', 'Done', 8, NULL),
(216, 'BTD202409041256233026', 5, 2, '2020-04-11', 'Done', 8, NULL),
(217, 'BTD202409041256233026', 5, 3, '2020-05-09', 'Done', 8, NULL),
(218, 'BTD202409041256233026', 5, 4, '2020-11-07', 'Done', 8, NULL),
(219, 'BTD202409041256233026', 6, 1, '2020-11-07', 'Done', 8, NULL),
(220, 'BTD202409041256233026', 7, 1, '2021-05-04', 'Done', 8, NULL),
(221, 'BTD202409042304163533', 1, 1, '2002-01-23', 'Pending', 9, NULL),
(222, 'BTD202409042304163533', 3, 1, '2002-03-05', 'Done', 9, 9),
(223, 'BTD202409042304163533', 3, 2, '2002-04-02', 'Done', 9, 9),
(224, 'BTD202409042304163533', 3, 3, '2002-04-30', 'Done', 9, 9),
(225, 'BTD202409042304163533', 4, 1, '2002-03-05', 'Done', 9, 9),
(226, 'BTD202409042304163533', 4, 2, '2002-04-02', 'Done', 9, 9),
(227, 'BTD202409042304163533', 4, 3, '2002-04-30', 'Done', 9, 9),
(228, 'BTD202409042304163533', 5, 1, '2002-03-05', 'Done', 9, 9),
(229, 'BTD202409042304163533', 5, 2, '2002-04-02', 'Done', 9, 9),
(230, 'BTD202409042304163533', 5, 3, '2002-04-30', 'Done', 9, 9),
(231, 'BTD202409042304163533', 5, 4, '2002-10-29', 'Pending', 9, NULL),
(232, 'BTD202409042304163533', 6, 1, '2002-10-29', 'Pending', 9, NULL),
(233, 'BTD202409042304163533', 7, 1, '2003-04-25', 'Done', 9, 9),
(234, 'BTD202502181939223387', 1, 1, '2025-02-19', 'Pending', 9, NULL),
(235, 'BTD202502181939223387', 3, 1, '2025-04-01', 'Pending', 9, NULL),
(236, 'BTD202502181939223387', 3, 2, '2025-04-29', 'Pending', 9, NULL),
(237, 'BTD202502181939223387', 3, 3, '2025-05-27', 'Pending', 9, NULL),
(238, 'BTD202502181939223387', 4, 1, '2025-04-01', 'Pending', 9, NULL),
(239, 'BTD202502181939223387', 4, 2, '2025-04-29', 'Pending', 9, NULL),
(240, 'BTD202502181939223387', 4, 3, '2025-05-27', 'Pending', 9, NULL),
(241, 'BTD202502181939223387', 5, 1, '2025-04-01', 'Pending', 9, NULL),
(242, 'BTD202502181939223387', 5, 2, '2025-04-29', 'Pending', 9, NULL),
(243, 'BTD202502181939223387', 5, 3, '2025-05-27', 'Pending', 9, NULL),
(244, 'BTD202502181939223387', 5, 4, '2025-11-25', 'Pending', 9, NULL),
(245, 'BTD202502181939223387', 6, 1, '2025-11-25', 'Pending', 9, NULL),
(246, 'BTD202502181939223387', 7, 1, '2026-05-22', 'Pending', 9, NULL),
(247, 'BTD202502181941123798', 1, 1, '2025-02-19', 'Pending', 9, NULL),
(248, 'BTD202502181941123798', 3, 1, '2025-04-01', 'Pending', 9, NULL),
(249, 'BTD202502181941123798', 3, 2, '2025-04-29', 'Pending', 9, NULL),
(250, 'BTD202502181941123798', 3, 3, '2025-05-27', 'Pending', 9, NULL),
(251, 'BTD202502181941123798', 4, 1, '2025-04-01', 'Pending', 9, NULL),
(252, 'BTD202502181941123798', 4, 2, '2025-04-29', 'Pending', 9, NULL),
(253, 'BTD202502181941123798', 4, 3, '2025-05-27', 'Pending', 9, NULL),
(254, 'BTD202502181941123798', 5, 1, '2025-04-01', 'Pending', 9, NULL),
(255, 'BTD202502181941123798', 5, 2, '2025-04-29', 'Pending', 9, NULL),
(256, 'BTD202502181941123798', 5, 3, '2025-05-27', 'Pending', 9, NULL),
(257, 'BTD202502181941123798', 5, 4, '2025-11-25', 'Pending', 9, NULL),
(258, 'BTD202502181941123798', 6, 1, '2025-11-25', 'Pending', 9, NULL),
(259, 'BTD202502181941123798', 7, 1, '2026-05-22', 'Pending', 9, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `vaccine`
--

CREATE TABLE `vaccine` (
  `id` int(11) NOT NULL,
  `vaccine_name` varchar(255) NOT NULL,
  `vaccine_code` varchar(100) NOT NULL,
  `doses` int(11) NOT NULL,
  `time_intervals` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`time_intervals`)),
  `manufactured_country` varchar(100) NOT NULL,
  `disease` varchar(255) NOT NULL,
  `storage_temperature` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vaccine`
--

INSERT INTO `vaccine` (`id`, `vaccine_name`, `vaccine_code`, `doses`, `time_intervals`, `manufactured_country`, `disease`, `storage_temperature`, `created_at`) VALUES
(1, '', '', 0, '[]', '', '', '', '2025-02-19 08:20:13'),
(3, 'Penatvalent Vaccine', 'PENTA505', 3, '[\"42\",\"70\",\"98\"]', 'GlaxoSmithKline(UK)', 'DIptheria,Tetanus,Perthussis,Hepatitis B,Influenzae Type B', '2 - 4 Degree', '2024-09-04 08:46:24'),
(4, 'PCV', 'PCV404', 3, '[\"42\",\"70\",\"98\"]', 'GlaxoSmithKline(UK)', 'Polio', '2 - 8 Degree', '2024-09-04 08:48:51'),
(5, 'Oral Polio Vaccine (OPV)', 'OPV101', 4, '[\"42\",\"70\",\"98\",\"280\"]', 'Sanofi Pasteur(French)', 'Polio', '-20 - (2-8) Degree', '2024-09-04 08:53:39'),
(6, 'MR Vaccine', 'MR403', 1, '[\"280\"]', 'Sanofi Pasteur(French)', 'Measles,Rubella', '2 - 8 Degree', '2024-09-04 09:03:30'),
(7, 'Measeles Vaccine', 'MV503', 1, '[\"458\"]', 'GlaxoSmithKline(UK)', 'Measles', '2 - 8 Degree', '2024-09-04 09:05:29');

-- --------------------------------------------------------

--
-- Table structure for table `vaccine_status`
--

CREATE TABLE `vaccine_status` (
  `application_id` varchar(255) NOT NULL,
  `status` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vaccine_status`
--

INSERT INTO `vaccine_status` (`application_id`, `status`) VALUES
('BTD202409041256233026', 1),
('BTD202409042304163533', 0);

-- --------------------------------------------------------

--
-- Table structure for table `volunteers`
--

CREATE TABLE `volunteers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `healthcare` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `subdistrict_id` int(11) DEFAULT NULL,
  `healthcare_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `volunteers`
--

INSERT INTO `volunteers` (`id`, `name`, `email`, `healthcare`, `password`, `subdistrict_id`, `healthcare_id`) VALUES
(5, 'Sudip Singho', 'sudip@btd.gov', 'parkview medical college', '$2y$10$S6sRQHbdBWPQm0GscntvG.Uimst5lnLsYyZPZajZmffoKmPzryFPS', 240001, 8),
(7, 'pritom', 'pritom@btd.gov', 'MAG osmani medical', '$2y$10$S6sRQHbdBWPQm0GscntvG.Uimst5lnLsYyZPZajZmffoKmPzryFPS', 240001, 9),
(8, 'sadi', 'sadi@btd.gov', 'MAG osmani medical', '$2y$10$S6sRQHbdBWPQm0GscntvG.Uimst5lnLsYyZPZajZmffoKmPzryFPS', 240001, 9),
(9, 'partho', 'partho@gmail.com', 'MAG osmani medical', 'partho', 240001, 9);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `division_id` (`division_id`),
  ADD KEY `district_id` (`district_id`),
  ADD KEY `subdistrict_id` (`subdistrict_id`);

--
-- Indexes for table `allowance_applicant`
--
ALTER TABLE `allowance_applicant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nid_number` (`nid_number`),
  ADD KEY `citizen_id` (`citizen_id`),
  ADD KEY `idx_allowance_nid` (`nid_number`),
  ADD KEY `idx_allowance_status` (`status`);

--
-- Indexes for table `applicants`
--
ALTER TABLE `applicants`
  ADD PRIMARY KEY (`application_id`),
  ADD KEY `birth_division_id` (`birth_division_id`),
  ADD KEY `birth_district_id` (`birth_district_id`),
  ADD KEY `birth_subdistrict_id` (`birth_subdistrict_id`),
  ADD KEY `division_id` (`division_id`),
  ADD KEY `district_id` (`district_id`),
  ADD KEY `subdistrict_id` (`subdistrict_id`),
  ADD KEY `healthcare_id` (`healthcare_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `baby_reg`
--
ALTER TABLE `baby_reg`
  ADD PRIMARY KEY (`reg_no`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- Indexes for table `citizen`
--
ALTER TABLE `citizen`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `citizen_report`
--
ALTER TABLE `citizen_report`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_monthly_report` (`volunteer_id`,`healthcare_center_id`,`month`),
  ADD KEY `healthcare_center_id` (`healthcare_center_id`),
  ADD KEY `subdistrict_id` (`subdistrict_id`);

--
-- Indexes for table `districts`
--
ALTER TABLE `districts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `division_id` (`division_id`);

--
-- Indexes for table `divisions`
--
ALTER TABLE `divisions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `healthcare`
--
ALTER TABLE `healthcare`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `nid_applicant`
--
ALTER TABLE `nid_applicant`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `nid_verification`
--
ALTER TABLE `nid_verification`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `nid_number` (`nid_number`);

--
-- Indexes for table `passport_applicant`
--
ALTER TABLE `passport_applicant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nid_number` (`nid_number`),
  ADD UNIQUE KEY `tracking_number` (`tracking_number`);

--
-- Indexes for table `passport_verification`
--
ALTER TABLE `passport_verification`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `passport_number` (`passport_number`),
  ADD KEY `user` (`application_id`);

--
-- Indexes for table `subdistricts`
--
ALTER TABLE `subdistricts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `district_id` (`district_id`);

--
-- Indexes for table `vaccination_schedule`
--
ALTER TABLE `vaccination_schedule`
  ADD PRIMARY KEY (`id`),
  ADD KEY `applicant_id` (`application_id`),
  ADD KEY `healthcare_id` (`healthcare_id`),
  ADD KEY `sgfrsg` (`volunteer_id`),
  ADD KEY `vaccination_schedule_ibfk_2` (`vaccine_id`);

--
-- Indexes for table `vaccine`
--
ALTER TABLE `vaccine`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `vaccine_code` (`vaccine_code`);

--
-- Indexes for table `vaccine_status`
--
ALTER TABLE `vaccine_status`
  ADD PRIMARY KEY (`application_id`);

--
-- Indexes for table `volunteers`
--
ALTER TABLE `volunteers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=240006;

--
-- AUTO_INCREMENT for table `allowance_applicant`
--
ALTER TABLE `allowance_applicant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `baby_reg`
--
ALTER TABLE `baby_reg`
  MODIFY `reg_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `citizen`
--
ALTER TABLE `citizen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `citizen_report`
--
ALTER TABLE `citizen_report`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `healthcare`
--
ALTER TABLE `healthcare`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `nid_applicant`
--
ALTER TABLE `nid_applicant`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `nid_verification`
--
ALTER TABLE `nid_verification`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `passport_applicant`
--
ALTER TABLE `passport_applicant`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `passport_verification`
--
ALTER TABLE `passport_verification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `vaccination_schedule`
--
ALTER TABLE `vaccination_schedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=260;

--
-- AUTO_INCREMENT for table `vaccine`
--
ALTER TABLE `vaccine`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `volunteers`
--
ALTER TABLE `volunteers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admins`
--
ALTER TABLE `admins`
  ADD CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`),
  ADD CONSTRAINT `admins_ibfk_2` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`),
  ADD CONSTRAINT `admins_ibfk_3` FOREIGN KEY (`subdistrict_id`) REFERENCES `subdistricts` (`id`);

--
-- Constraints for table `allowance_applicant`
--
ALTER TABLE `allowance_applicant`
  ADD CONSTRAINT `allowance_applicant_ibfk_1` FOREIGN KEY (`citizen_id`) REFERENCES `citizen` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `applicants`
--
ALTER TABLE `applicants`
  ADD CONSTRAINT `applicants_ibfk_1` FOREIGN KEY (`birth_division_id`) REFERENCES `divisions` (`id`),
  ADD CONSTRAINT `applicants_ibfk_2` FOREIGN KEY (`birth_district_id`) REFERENCES `districts` (`id`),
  ADD CONSTRAINT `applicants_ibfk_3` FOREIGN KEY (`birth_subdistrict_id`) REFERENCES `subdistricts` (`id`),
  ADD CONSTRAINT `applicants_ibfk_4` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`),
  ADD CONSTRAINT `applicants_ibfk_5` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`),
  ADD CONSTRAINT `applicants_ibfk_6` FOREIGN KEY (`subdistrict_id`) REFERENCES `subdistricts` (`id`),
  ADD CONSTRAINT `applicants_ibfk_7` FOREIGN KEY (`healthcare_id`) REFERENCES `healthcare` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `citizen_report`
--
ALTER TABLE `citizen_report`
  ADD CONSTRAINT `citizen_report_ibfk_1` FOREIGN KEY (`volunteer_id`) REFERENCES `volunteers` (`id`),
  ADD CONSTRAINT `citizen_report_ibfk_2` FOREIGN KEY (`healthcare_center_id`) REFERENCES `healthcare` (`id`),
  ADD CONSTRAINT `citizen_report_ibfk_3` FOREIGN KEY (`subdistrict_id`) REFERENCES `subdistricts` (`id`);

--
-- Constraints for table `districts`
--
ALTER TABLE `districts`
  ADD CONSTRAINT `districts_ibfk_1` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `passport_verification`
--
ALTER TABLE `passport_verification`
  ADD CONSTRAINT `user` FOREIGN KEY (`application_id`) REFERENCES `passport_applicant` (`id`);

--
-- Constraints for table `subdistricts`
--
ALTER TABLE `subdistricts`
  ADD CONSTRAINT `subdistricts_ibfk_1` FOREIGN KEY (`district_id`) REFERENCES `districts` (`id`);

--
-- Constraints for table `vaccination_schedule`
--
ALTER TABLE `vaccination_schedule`
  ADD CONSTRAINT `sgfrsg` FOREIGN KEY (`volunteer_id`) REFERENCES `volunteers` (`id`),
  ADD CONSTRAINT `vaccination_schedule_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applicants` (`application_id`),
  ADD CONSTRAINT `vaccination_schedule_ibfk_2` FOREIGN KEY (`vaccine_id`) REFERENCES `vaccine` (`id`),
  ADD CONSTRAINT `vaccination_schedule_ibfk_3` FOREIGN KEY (`healthcare_id`) REFERENCES `healthcare` (`id`);

--
-- Constraints for table `vaccine_status`
--
ALTER TABLE `vaccine_status`
  ADD CONSTRAINT `vaccine_status_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `applicants` (`application_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
