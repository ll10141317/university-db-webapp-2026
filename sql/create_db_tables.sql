/*==============================================================*/
/* DBMS name:      openGauss 6.0.2                              */
/* 用途:           实验05 大学数据库 - 建表脚本                  */
/* 执行方式:       gsql -d studentdb -U student -W xxx -r        */
/*                 \set AUTOCOMMIT off                           */
/*                 \i create_db_tables.sql                       */
/*==============================================================*/
drop table if exists ADVISOR;
drop table if exists TAKES;
drop table if exists TEACHES;
drop table if exists PREREQ;
drop table if exists SECTION;
drop table if exists COURSE;
drop table if exists INSTRUCTOR;
drop table if exists STUDENT;
drop table if exists DEPARTMENT;
drop table if exists TIME_SLOT;
drop table if exists CLASSROOM;

/* Table: CLASSROOM */
create table CLASSROOM
(
   BUILDING             varchar(15) not null,
   ROOM_NUMBER          varchar(7) not null,
   CAPACITY             numeric(4,0),
   primary key (BUILDING, ROOM_NUMBER)
);

/* Table: DEPARTMENT */
create table DEPARTMENT
(
   DEPT_NAME            varchar(20) not null,
   BUILDING             varchar(15),
   BUDGET               numeric(12,2),
   primary key (DEPT_NAME)
);

/* Table: COURSE */
create table COURSE
(
   COURSE_ID            varchar(8) not null,
   DEPT_NAME            varchar(20),
   TITLE                varchar(50),
   CREDITS              numeric(2,0),
   primary key (COURSE_ID)
);

/* Table: INSTRUCTOR */
create table INSTRUCTOR
(
   ID                   varchar(5) not null,
   DEPT_NAME            varchar(20),
   NAME                 varchar(20) not null,
   SALARY               numeric(8,2),
   primary key (ID)
);

/* Table: STUDENT */
create table STUDENT
(
   ID                   varchar(5) not null,
   DEPT_NAME            varchar(20),
   NAME                 varchar(20) not null,
   TOT_CRED             numeric(3,0),
   primary key (ID)
);

/* Table: SECTION */
create table SECTION
(
   COURSE_ID            varchar(8) not null,
   SEC_ID               varchar(8) not null,
   SEMESTER             varchar(6) not null,
   YEAR                 numeric(4,0) not null,
   BUILDING             varchar(15),
   ROOM_NUMBER          varchar(7),
   TIME_SLOT_ID         varchar(4),
   primary key (COURSE_ID, SEC_ID, SEMESTER, YEAR)
);

/* Table: TAKES */
create table TAKES
(
   ID                   varchar(5) not null,
   COURSE_ID            varchar(8) not null,
   SEC_ID               varchar(8) not null,
   SEMESTER             varchar(6) not null,
   YEAR                 numeric(4,0) not null,
   GRADE                varchar(2),
   primary key (COURSE_ID, ID, SEC_ID, SEMESTER, YEAR)
);

/* Table: TEACHES */
create table TEACHES
(
   ID                   varchar(5) not null,
   COURSE_ID            varchar(8) not null,
   SEC_ID               varchar(8) not null,
   SEMESTER             varchar(6) not null,
   YEAR                 numeric(4,0) not null,
   primary key (ID, COURSE_ID, SEC_ID, SEMESTER, YEAR)
);

/* Table: ADVISOR */
create table ADVISOR
(
   STU_ID               varchar(5) not null,
   ID                   varchar(5),
   primary key (STU_ID)
);

/* Table: PREREQ */
create table PREREQ
(
   COURSE_ID            varchar(8) not null,
   PRE_COURSE_ID        varchar(8) not null,
   primary key (COURSE_ID, PRE_COURSE_ID)
);

/* Table: TIME_SLOT */
create table TIME_SLOT
(
   TIME_SLOT_ID         varchar(4) not null,
   DAY                  varchar(1) not null,
   START_HR             numeric(2,0) not null,
   START_MIN            numeric(2,0) not null,
   END_HR               numeric(2,0),
   END_MIN              numeric(2,0),
   primary key (TIME_SLOT_ID, DAY, START_HR, START_MIN)
);

/* 外键约束 */
alter table ADVISOR add constraint FK_ADVISOR_INST foreign key (ID)
      references INSTRUCTOR (ID) on delete restrict on update restrict;
alter table ADVISOR add constraint FK_ADVISOR_STU foreign key (STU_ID)
      references STUDENT (ID) on delete restrict on update restrict;
alter table COURSE add constraint FK_COURSE_DEPT foreign key (DEPT_NAME)
      references DEPARTMENT (DEPT_NAME) on delete restrict on update restrict;
alter table INSTRUCTOR add constraint FK_INST_DEPT foreign key (DEPT_NAME)
      references DEPARTMENT (DEPT_NAME) on delete restrict on update restrict;
alter table PREREQ add constraint FK_PREREQ_COURSE foreign key (COURSE_ID)
      references COURSE (COURSE_ID) on delete restrict on update restrict;
alter table PREREQ add constraint FK_PREREQ_PRE foreign key (PRE_COURSE_ID)
      references COURSE (COURSE_ID) on delete restrict on update restrict;
alter table SECTION add constraint FK_SECTION_COURSE foreign key (COURSE_ID)
      references COURSE (COURSE_ID) on delete restrict on update restrict;
alter table SECTION add constraint FK_SECTION_CLASSROOM foreign key (BUILDING, ROOM_NUMBER)
      references CLASSROOM (BUILDING, ROOM_NUMBER) on delete restrict on update restrict;
alter table STUDENT add constraint FK_STUDENT_DEPT foreign key (DEPT_NAME)
      references DEPARTMENT (DEPT_NAME) on delete restrict on update restrict;
alter table TAKES add constraint FK_TAKES_SECTION foreign key (COURSE_ID, SEC_ID, SEMESTER, YEAR)
      references SECTION (COURSE_ID, SEC_ID, SEMESTER, YEAR) on delete restrict on update restrict;
alter table TAKES add constraint FK_TAKES_STUDENT foreign key (ID)
      references STUDENT (ID) on delete restrict on update restrict;
alter table TEACHES add constraint FK_TEACHES_INST foreign key (ID)
      references INSTRUCTOR (ID) on delete restrict on update restrict;
alter table TEACHES add constraint FK_TEACHES_SECTION foreign key (COURSE_ID, SEC_ID, SEMESTER, YEAR)
      references SECTION (COURSE_ID, SEC_ID, SEMESTER, YEAR) on delete restrict on update restrict;
