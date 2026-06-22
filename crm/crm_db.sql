-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 22, 2026 at 02:03 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `crm_db`
--

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
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Customer', 7, 'add_customer'),
(26, 'Can change Customer', 7, 'change_customer'),
(27, 'Can delete Customer', 7, 'delete_customer'),
(28, 'Can view Customer', 7, 'view_customer'),
(29, 'Can add customer stage history', 8, 'add_customerstagehistory'),
(30, 'Can change customer stage history', 8, 'change_customerstagehistory'),
(31, 'Can delete customer stage history', 8, 'delete_customerstagehistory'),
(32, 'Can view customer stage history', 8, 'view_customerstagehistory'),
(33, 'Can add monthly sales statistics', 9, 'add_monthlysalesstatistics'),
(34, 'Can change monthly sales statistics', 9, 'change_monthlysalesstatistics'),
(35, 'Can delete monthly sales statistics', 9, 'delete_monthlysalesstatistics'),
(36, 'Can view monthly sales statistics', 9, 'view_monthlysalesstatistics'),
(37, 'Can add permission grant', 10, 'add_permissiongrant'),
(38, 'Can change permission grant', 10, 'change_permissiongrant'),
(39, 'Can delete permission grant', 10, 'delete_permissiongrant'),
(40, 'Can view permission grant', 10, 'view_permissiongrant'),
(41, 'Can add sales team mapping', 11, 'add_salesteammapping'),
(42, 'Can change sales team mapping', 11, 'change_salesteammapping'),
(43, 'Can delete sales team mapping', 11, 'delete_salesteammapping'),
(44, 'Can view sales team mapping', 11, 'view_salesteammapping'),
(45, 'Can add user role', 12, 'add_userrole'),
(46, 'Can change user role', 12, 'change_userrole'),
(47, 'Can delete user role', 12, 'delete_userrole'),
(48, 'Can view user role', 12, 'view_userrole');

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

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$720000$nxV5xCerxqTtNIMoxDGngn$/xjCn681AdWN9E0Ld7yUmtUg7toc2Cm7nr5KmUUAw3I=', '2026-06-22 00:01:36.764073', 1, 'owner', '', '', 'owner@gmail.com', 1, 1, '2026-06-21 23:39:53.651269');

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
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'webapp', 'customer'),
(8, 'webapp', 'customerstagehistory'),
(9, 'webapp', 'monthlysalesstatistics'),
(10, 'webapp', 'permissiongrant'),
(11, 'webapp', 'salesteammapping'),
(12, 'webapp', 'userrole');

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
(1, 'contenttypes', '0001_initial', '2026-06-21 23:06:09.166956'),
(2, 'auth', '0001_initial', '2026-06-21 23:06:09.486348'),
(3, 'admin', '0001_initial', '2026-06-21 23:06:09.552574'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-06-21 23:06:09.558374'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-06-21 23:06:09.564117'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-06-21 23:06:09.611352'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-06-21 23:06:09.651186'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-06-21 23:06:09.660567'),
(9, 'auth', '0004_alter_user_username_opts', '2026-06-21 23:06:09.666652'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-06-21 23:06:09.701812'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-06-21 23:06:09.702987'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-06-21 23:06:09.708691'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-06-21 23:06:09.717492'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-06-21 23:06:09.728480'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-06-21 23:06:09.743250'),
(16, 'auth', '0011_update_proxy_permissions', '2026-06-21 23:06:09.750746'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-06-21 23:06:09.759442'),
(18, 'sessions', '0001_initial', '2026-06-21 23:06:09.782376'),
(19, 'webapp', '0001_initial', '2026-06-21 23:06:09.790292'),
(20, 'webapp', '0002_customer_customerstagehistory_monthlysalesstatistics_and_more', '2026-06-21 23:06:10.199171');

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
('x2hjgbn0n7s3btk817jwadjn2jixj5nv', 'e30:1wbS6f:1MADHbBeLnZt4P9zyVARxX6uB-FN1IQYn83rF67TGl8', '2026-07-06 00:01:41.488461');

-- --------------------------------------------------------

--
-- Table structure for table `webapp_customer`
--

CREATE TABLE `webapp_customer` (
  `id` bigint(20) NOT NULL,
  `first_name` varchar(250) NOT NULL,
  `last_name` varchar(250) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `request` longtext NOT NULL,
  `customer_type` varchar(20) NOT NULL,
  `current_stage` varchar(30) NOT NULL,
  `stage_start_date` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `sales_rep_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `webapp_customerstagehistory`
--

CREATE TABLE `webapp_customerstagehistory` (
  `id` bigint(20) NOT NULL,
  `previous_stage` varchar(30) NOT NULL,
  `new_stage` varchar(30) NOT NULL,
  `changed_at` datetime(6) NOT NULL,
  `customer_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `webapp_monthlysalesstatistics`
--

CREATE TABLE `webapp_monthlysalesstatistics` (
  `id` bigint(20) NOT NULL,
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `customers_acquired` int(11) NOT NULL,
  `contracts_signed` int(11) NOT NULL,
  `sales_rep_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `webapp_permissiongrant`
--

CREATE TABLE `webapp_permissiongrant` (
  `id` bigint(20) NOT NULL,
  `permission` varchar(20) NOT NULL,
  `granted_to_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `webapp_salesteammapping`
--

CREATE TABLE `webapp_salesteammapping` (
  `id` bigint(20) NOT NULL,
  `assigned_date` datetime(6) NOT NULL,
  `sales_id` int(11) NOT NULL,
  `team_leader_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `webapp_userrole`
--

CREATE TABLE `webapp_userrole` (
  `id` bigint(20) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `team_number` varchar(50) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `webapp_userrole`
--

INSERT INTO `webapp_userrole` (`id`, `phone`, `team_number`, `role`, `is_approved`, `created_at`, `user_id`) VALUES
(1, NULL, NULL, 'owner', 1, '2026-06-22 03:00:02.000000', 1);

--
-- Indexes for dumped tables
--

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
-- Indexes for table `webapp_customer`
--
ALTER TABLE `webapp_customer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `webapp_customer_sales_rep_id_phone_c447401e_uniq` (`sales_rep_id`,`phone`);

--
-- Indexes for table `webapp_customerstagehistory`
--
ALTER TABLE `webapp_customerstagehistory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `webapp_customerstage_customer_id_af1ab2ae_fk_webapp_cu` (`customer_id`);

--
-- Indexes for table `webapp_monthlysalesstatistics`
--
ALTER TABLE `webapp_monthlysalesstatistics`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `webapp_monthlysalesstati_sales_rep_id_year_month_c729f209_uniq` (`sales_rep_id`,`year`,`month`);

--
-- Indexes for table `webapp_permissiongrant`
--
ALTER TABLE `webapp_permissiongrant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `webapp_permissiongrant_granted_to_id_permission_7f966722_uniq` (`granted_to_id`,`permission`);

--
-- Indexes for table `webapp_salesteammapping`
--
ALTER TABLE `webapp_salesteammapping`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sales_id` (`sales_id`),
  ADD KEY `webapp_salesteammapping_team_leader_id_dae33cae_fk_auth_user_id` (`team_leader_id`);

--
-- Indexes for table `webapp_userrole`
--
ALTER TABLE `webapp_userrole`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `webapp_customer`
--
ALTER TABLE `webapp_customer`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `webapp_customerstagehistory`
--
ALTER TABLE `webapp_customerstagehistory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `webapp_monthlysalesstatistics`
--
ALTER TABLE `webapp_monthlysalesstatistics`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `webapp_permissiongrant`
--
ALTER TABLE `webapp_permissiongrant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `webapp_salesteammapping`
--
ALTER TABLE `webapp_salesteammapping`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `webapp_userrole`
--
ALTER TABLE `webapp_userrole`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

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
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `webapp_customer`
--
ALTER TABLE `webapp_customer`
  ADD CONSTRAINT `webapp_customer_sales_rep_id_ec06af72_fk_auth_user_id` FOREIGN KEY (`sales_rep_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `webapp_customerstagehistory`
--
ALTER TABLE `webapp_customerstagehistory`
  ADD CONSTRAINT `webapp_customerstage_customer_id_af1ab2ae_fk_webapp_cu` FOREIGN KEY (`customer_id`) REFERENCES `webapp_customer` (`id`);

--
-- Constraints for table `webapp_monthlysalesstatistics`
--
ALTER TABLE `webapp_monthlysalesstatistics`
  ADD CONSTRAINT `webapp_monthlysaless_sales_rep_id_c54b1462_fk_auth_user` FOREIGN KEY (`sales_rep_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `webapp_permissiongrant`
--
ALTER TABLE `webapp_permissiongrant`
  ADD CONSTRAINT `webapp_permissiongrant_granted_to_id_c79da9b4_fk_auth_user_id` FOREIGN KEY (`granted_to_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `webapp_salesteammapping`
--
ALTER TABLE `webapp_salesteammapping`
  ADD CONSTRAINT `webapp_salesteammapping_sales_id_8948c624_fk_auth_user_id` FOREIGN KEY (`sales_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `webapp_salesteammapping_team_leader_id_dae33cae_fk_auth_user_id` FOREIGN KEY (`team_leader_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `webapp_userrole`
--
ALTER TABLE `webapp_userrole`
  ADD CONSTRAINT `webapp_userrole_user_id_8b5874ec_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
