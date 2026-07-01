-- Core reference tables for the MHSDS synthetic data warehouse.

USE MHSDS_DW;
GO

-- 1. services: the mental health services offered

IF OBJECT_ID('dbo.services','U') IS NULL
BEGIN
    CREATE TABLE dbo.services (
        service_id      INT             NOT NULL,
        service_name    VARCHAR(100)    NOT NULL,
        service_type    VARCHAR(50)     NULL,
        CONSTRAINT PK_services PRIMARY KEY(service_id)
    );
END;
GO

-- 2. teams: clinical teams, each belonging to one service. 

IF OBJECT_ID('dbo.teams','U') IS NULL
BEGIN
    CREATE TABLE dbo.teams (
        team_id         INT             NOT NULL,
        team_name       VARCHAR(100)    NOT NULL,
        service_id      INT             NOT NULL,
        CONSTRAINT PK_teams PRIMARY KEY(team_id),
        CONSTRAINT FK_teams_services FOREIGN KEY(service_id) REFERENCES dbo.services(service_id)
    );
END;
GO

-- SELECT * FROM dbo.services;
-- SELECT * FROM dbo.teams;