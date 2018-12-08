DROP TABLE IF EXISTS Appointment;
DROP TABLE IF EXISTS Physician;
CREATE TABLE PHYSICIAN (
  PID INTEGER,
  FNAME varchar(30),
  LNAME varchar(30),
  PRIMARY KEY (PID)
);
CREATE TABLE APPOINTMENT (
  AID INTEGER,
  PFNAME varchar(30),
  PLNAME varchar(30),
  APPDATE varchar(20),
  APPTIME varchar(20),
  APPTYPE varchar(20),
  PID INTEGER,
  FOREIGN KEY (PID) references PHYSICIAN(PID)
);

insert into PHYSICIAN values (1,'Naveen','RAJ');
insert into PHYSICIAN values (2,'Bob','Smith');
insert into PHYSICIAN values (3,'Joe','Jones');

insert into APPOINTMENT values (1,'Alex','Smith','12-10-2018', '10:00','New Patient',3);
insert into APPOINTMENT values (2,'Josh','Jones','12-11-2018','15:15','Follow-Up',2);
insert into APPOINTMENT values (3,'Matt','Ryan','12-15-2018','11:30','New Patient',3);
insert into APPOINTMENT values (4,'Alex','Joe','12-10-2018', '15:10','New Patient',3);
