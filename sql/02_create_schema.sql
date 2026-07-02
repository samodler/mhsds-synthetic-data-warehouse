-- Core reference tables for the MHSDS synthetic data warehouse.

USE MHSDS_DW;
GO

-- services: the mental health services offered

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

-- teams: clinical teams, each belonging to one service. 

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

-- patients
/* 
    Non PK fields are intentionally nullable and non-unique so that synthetic data-quality issues can exist and be detected by downstream validation.
*/
IF OBJECT_ID('dbo.patients','U') IS NULL
BEGIN
    CREATE TABLE dbo.patients(
        patient_id          INT             NOT NULL,
        nhs_number          CHAR(10)        NULL,
        local_patient_id    VARCHAR(20)     NULL,
        date_of_birth       DATE            NULL,
        gender_code         VARCHAR(2)      NULL,
        ethnicity_code      VARCHAR(2)      NULL,
        postcode            VARCHAR(8)      NULL,
        CONSTRAINT PK_patients PRIMARY KEY (patient_id)
    );
END
GO
-- SELECT * FROM dbo.patients


-- referrals: the table linking a patient to a team for an episode of care
/*
    NOTE: team_id is nullable as missing team ID is a target data quality issue. There is deliberately no CHECK constraint on the dates, so that discharge before referral can occur in the data and be caught by downstream validation, not blocked at load time.
*/

IF OBJECT_ID('dbo.referrals', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.referrals (
        referral_id     INT   NOT NULL,
        patient_id      INT   NOT NULL,
        team_id         INT   NULL,
        referral_date   DATE  NOT NULL,
        discharge_date  DATE  NULL,
        CONSTRAINT PK_referrals PRIMARY KEY (referral_id),
        CONSTRAINT FK_referrals_patients FOREIGN KEY (patient_id)
            REFERENCES dbo.patients (patient_id),
        CONSTRAINT FK_referrals_teams FOREIGN KEY (team_id)
            REFERENCES dbo.teams (team_id)
    );
END
GO

-- SELECT * FROM dbo.referrals;

-- SELECT * FROM sys.foreign_keys fk
-- SELECT * FROM sys.tables tp

-- sys.foreign_keys.parent_object_id = the table that contains the FK column (child table)
-- sys.foreign_keys.referenced_object_id = the table being referenced by the FK (parent table)


SELECT fk.name as fk_name, ct.name as child_table, pt.name as parent_table
FROM sys.foreign_keys fk
JOIN sys.tables ct ON fk.parent_object_id = ct.object_id
JOIN sys.tables pt ON fk.referenced_object_id = pt.object_id
WHERE ct.name = 'referrals';
