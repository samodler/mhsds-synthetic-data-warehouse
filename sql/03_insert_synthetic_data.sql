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

SELECT * FROM dbo.services
