SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `Department` (
  `dept_id` int NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`dept_id`)
);

INSERT INTO `Department` (`dept_id`, `name`) VALUES
  (1, "Computer Science"),
  (2, "Mathematics");

CREATE TABLE `Venue` (
  `venue_id` int NOT NULL,
  `location` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`venue_id`)
);

INSERT INTO `Venue` (`venue_id`, `location`) VALUES
(1, "MWT1"),
(2, "CPD-3.04"),
(3, "KB-223");

CREATE TABLE `Course` (
  `course_id` VARCHAR(8) NOT NULL,
  `dept_id` int NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`course_id`),
  FOREIGN KEY (`dept_id`) REFERENCES `Department` (`dept_id`)
);

INSERT INTO `Course` (`course_id`, `dept_id`, `name`) VALUES
  ("COMP3278", 1, "Introduction to database management systems"),
  ("COMP3258", 1, "Functional programming"),
  ("COMP3297", 1, "Software engineering"),
  ("MATH2014", 2, "Multivariable calculus and linear algebra");

CREATE TABLE `Class` (
  `class_id` int NOT NULL,
  `course_id` VARCHAR(8) NOT NULL,
  `zoom_link` text,
  `zoom_meeting_id` VARCHAR(10),
  `zoom_password` VARCHAR(10),
  PRIMARY KEY (`class_id`, `course_id`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
);

INSERT INTO `Class` (`class_id`, `course_id`, `zoom_link`, `zoom_meeting_id`, `zoom_password`) VALUES
  (1, "COMP3278", "https://zoom.us/comp3278", "01234567890", "123456"),
  (1, "COMP3258", "https://zoom.us/comp3258", "12312341234", "123456"),
  (1, "COMP3297", "https://zoom.us/comp3297", "32143214321", "123456"),
  (1, "MATH2014", "https://zoom.us/math2014", "98765431234", "123456");

CREATE TABLE `Lecture` (
  `lecture_id` int NOT NULL,
  `class_id` int NOT NULL,
  `course_id` VARCHAR(8) NOT NULL,
  `venue_id` int NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `weekday` int NOT NULL,
  PRIMARY KEY (`lecture_id`, `class_id`, `course_id`),
  FOREIGN KEY (`class_id`) REFERENCES `Class` (`class_id`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`),
  FOREIGN KEY (`venue_id`) REFERENCES `Venue` (`venue_id`)
);

INSERT INTO `Lecture` (`lecture_id`, `class_id`, `course_id`, `venue_id`, `start_time`, `end_time`, `weekday`) VALUES
(1, 1, "COMP3278", 1, "14:30:00", "15:20:00", 1),
(2, 1, "COMP3278", 1, "13:30:00", "15:20:00", 4),
(1, 1, "COMP3258", 2, "13:30:00", "15:20:00", 2),
(2, 1, "COMP3258", 2, "14:30:00", "15:20:00", 5),
(1, 1, "COMP3297", 3, "16:30:00", "18:20:00", 2),
(2, 1, "COMP3297", 3, "17:30:00", "18:20:00", 5),
(1, 1, "MATH2014", 3, "10:30:00", "12:20:00", 2),
(2, 1, "MATH2014", 3, "11:30:00", "12:20:00", 5);

CREATE TABLE `Student` (
  `student_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `cirriculum` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`student_id`)
);

INSERT INTO `Student` (`student_id`, `name`, `login_time`, `login_date`, `email`, `cirriculum`) VALUES
  (1, "Ng Ching Lap", NOW(), "2023-11-21", "ngcl1013@connect.hku.hk", "BBA(IS)"),
  (2, "Li Chi Tat", NOW(), "2023-11-21", "samlct@connect.hku.hk", "BSc(DA)"),
  (3, "Othmane Lkhalidi", NOW(), "2023-11-21", "u3617458@connect.hku.hk", "BEng(CS)");

CREATE TABLE `Instructor` (
  `instructor_id` int NOT NULL,
  `dept_id` int NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `email` VARCHAR(100),
  `office_location` VARCHAR(50),
  `office_hour_start` time,
  `office_hour_end` time,
  `office_hour_weekday` int,
  PRIMARY KEY(`instructor_id`),
  FOREIGN KEY(`dept_id`)REFERENCES `Department`(`dept_id`)
);

INSERT INTO `Instructor` (`instructor_id`, `dept_id`, `name`, `email`, `office_location`, `office_hour_start`, `office_hour_end`, `office_hour_weekday`) VALUES
  (1, 1, "Dr. Ping Luo", "pluo@cs.hku.hk", "CB-326", "10:00:00", "11:00:00", 1),
  (2, 1, "Dr. Oliveira, Bruno", "bruno@cs.hku.hk", "CB-420", "16:00:00", "17:00:00", 5),
  (3, 1, "Dr. Leo Yeung", "leocyyeung@connect.hku.hk", "CB-311", "15:30:00", "16:20:00", 2),
  (4, 2, "Dr. Haiyu Zhang", "zhhy118@hku.hk", "Room 311, Run Run Shaw Building", "09:00:00", "10:00:00", 2);

CREATE TABLE `Enroll` (
  `student_id` int NOT NULL,
  `class_id` int NOT NULL,
  `course_id` VARCHAR(8) NOT NULL,
  PRIMARY KEY (`student_id`, `class_id`, `course_id`),
  FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`),
  FOREIGN KEY (`class_id`) REFERENCES `Class` (`class_id`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
);

INSERT INTO `Enroll` (`student_id`, `class_id`, `course_id`) VALUES
  (1, 1, "COMP3278"),
  (1, 1, "COMP3258"),
  (1, 1, "COMP3297"),
  (1, 1, "MATH2014");

CREATE TABLE `Teach` (
  `instructor_id` int NOT NULL,
  `class_id` int NOT NULL,
  `course_id` VARCHAR(8) NOT NULL,
  FOREIGN KEY (`instructor_id`) REFERENCES `Instructor` (`instructor_id`),
  FOREIGN KEY (`class_id`) REFERENCES `Class` (`class_id`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`),
  PRIMARY KEY (`instructor_id`, `class_id`, `course_id`)
);

INSERT INTO `Teach` (`instructor_id`, `class_id`, `course_id`) VALUES
  (1, 1, "COMP3278"),
  (2, 1, "COMP3258"),
  (3, 1, "COMP3297"),
  (4, 1, "MATH2014");

CREATE TABLE `TeacherMessage` (
  `class_id` int NOT NULL,
  `course_id` VARCHAR(8) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`class_id`, `course_id`),
  FOREIGN KEY (`class_id`) REFERENCES `Class` (`class_id`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
);

INSERT INTO `TeacherMessage` (`class_id`, `course_id`, `message`) VALUES
  (1, "COMP3278", "Please prepare your presenatations!"),
  (1, "COMP3258", "Hello."),
  (1, "COMP3297", "Hello."),
  (1, "MATH2014", "Hello.");

CREATE TABLE `Material` (
  `material_id` int NOT NULL,
  `class_id` int NOT NULL,
  `course_id` VARCHAR(8) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `link` text NOT NULL,
  PRIMARY KEY (`material_id`, `class_id`, `course_id`),
  FOREIGN KEY (`class_id`) REFERENCES `Class` (`class_id`),
  FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
);

INSERT INTO `Material` (`material_id`, `class_id`, `course_id`, `name`, `link`) VALUES
  (1, 1, "COMP3278", "Lecture Notes 1", "https://moodle.hku.hk/mod/resource/view.php?id=3081895"),
  (2, 1, "COMP3278", "Lecture Notes 2", "https://moodle.hku.hk/mod/resource/view.php?id=3081960"),
  (3, 1, "COMP3278", "Lecture Notes 3", "https://moodle.hku.hk/mod/resource/view.php?id=3095373"),
  (4, 1, "COMP3278", "Lecture Notes 4", "https://moodle.hku.hk/mod/resource/view.php?id=3095391"),

  (1, 1, "COMP3258", "Lecture Notes 1", "https://moodle.hku.hk/mod/resource/view.php?id=3077823"),
  (2, 1, "COMP3258", "Lecture Notes 2", "https://moodle.hku.hk/mod/resource/view.php?id=3077856"),
  (3, 1, "COMP3258", "Lecture Notes 3", "https://moodle.hku.hk/mod/resource/view.php?id=3092768"),
  (4, 1, "COMP3258", "Lecture Notes 4", "https://moodle.hku.hk/mod/resource/view.php?id=3111695"),

  (1, 1, "COMP3297", "Lecture Notes 1", "https://moodle.hku.hk/mod/resource/view.php?id=3087554"),
  (2, 1, "COMP3297", "Lecture Notes 2", "https://moodle.hku.hk/mod/resource/view.php?id=3087554"),
  (3, 1, "COMP3297", "Lecture Notes 3", "https://moodle.hku.hk/mod/resource/view.php?id=3116467"),
  (4, 1, "COMP3297", "Lecture Notes 4", "https://moodle.hku.hk/mod/resource/view.php?id=3131870"),

  (1, 1, "MATH2014", "Lecture Notes 1", "https://moodle.hku.hk/mod/resource/view.php?id=3038583"),
  (2, 1, "MATH2014", "Lecture Notes 2", "https://moodle.hku.hk/mod/resource/view.php?id=3038584"),
  (3, 1, "MATH2014", "Lecture Notes 3", "https://moodle.hku.hk/mod/resource/view.php?id=3038586"),
  (4, 1, "MATH2014", "Question Bank", "https://moodle.hku.hk/mod/resource/view.php?id=3038692"),