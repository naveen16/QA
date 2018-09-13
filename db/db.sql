DROP TABLE QA;
DROP TABLE SESSION; 
CREATE TABLE SESSION (
  SID INTEGER, 
  HostName varchar(20),
  StartTime varchar(20), 
  EndTime varchar(20),
  PRIMARY KEY (SID)
);
CREATE TABLE QA (
  SID INTEGER,
  QNO INTEGER,  
  Question varchar(20),
  Asked_By varchar(20), 
  Answer varchar(20), 
  Answer_URL varchar(20),
  Answered_By varchar(20),
  PRIMARY KEY (SID,QNO),
  FOREIGN KEY (SID) references SESSION(SID)
);

