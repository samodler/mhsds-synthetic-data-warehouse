USE MHSDS_DW;
GO

BULK INSERT dbo.services
FROM '/var/opt/mssql/import/services.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a', --hex for \r\n
    TABLOCK
);
GO

-- SELECT * FROM dbo.services

BULK INSERT dbo.teams
FROM '/var/opt/mssql/import/teams.csv'
WITH(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

-- SELECT * FROM dbo.teams

BULK INSERT dbo.patients
FROM '/var/opt/mssql/import/patients.csv'
WITH(
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO


/* SELECT 
    COUNT(*) AS total_patients,
    SUM(CASE WHEN postcode IS NULL THEN 1 ELSE 0 END) AS missing_postcode,
    SUM(CASE WHEN gender_code IS NULL THEN 1 ELSE 0 END) as missing_gender_code
FROM dbo.patients */

BULK INSERT dbo.referrals
FROM '/var/opt/mssql/import/referrals.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

/* SELECT
    COUNT(*) as total_referrals,
    SUM(CASE WHEN team_id IS NULL THEN 1 ELSE 0 END) as missing_team_id,
    SUM(CASE WHEN discharge_date < referral_date THEN 1 ELSE 0 END) as discharge_before_referral
FROM dbo.referrals */

/* SELECT 
    team_id,
    COUNT(referral_id) AS referrals_per_team
FROM dbo.referrals
GROUP BY team_id */

BULK INSERT dbo.care_contacts
FROM '/var/opt/mssql/import/care_contacts.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0d0a',
    TABLOCK
);
GO

SELECT
    COUNT(*) as total_contacts,
    -- cc.referral_id,
    -- cc.contact_date,
    -- r.referral_date
    SUM(CASE WHEN cc.contact_date < r.referral_date THEN 1 ELSE 0 END) AS contacts_before_referral
FROM dbo.care_contacts AS cc
JOIN dbo.referrals AS r
ON cc.referral_id = r.referral_id