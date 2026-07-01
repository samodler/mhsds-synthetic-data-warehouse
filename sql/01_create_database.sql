-- Creates the project database if it does not already exist.

IF DB_ID('MHSDS_DW') IS NULL
BEGIN
    CREATE DATABASE MHSDS_DW;
END
GO

USE MHSDS_DW;
GO

-- SELECT NAME FROM SYS.DATABASES ORDER BY NAME;