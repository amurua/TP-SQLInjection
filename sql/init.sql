/*
  init.sql - Script para preparar la base de datos de demostración
  Compatible con Microsoft SQL Server 2022
*/

IF DB_ID(N'DemoInjection') IS NOT NULL
BEGIN
    ALTER DATABASE DemoInjection SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DemoInjection;
END
GO

CREATE DATABASE DemoInjection;
GO

USE DemoInjection;
GO

CREATE TABLE dbo.Users (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Password NVARCHAR(100) NOT NULL,
    FullName NVARCHAR(100) NOT NULL
);
GO

INSERT INTO dbo.Users (Username, Password, FullName)
VALUES
    (N'alice', N'alice123', N'Alice Johnson'),
    (N'bob', N'p455w0rd', N'Bob Smith'),
    (N'carol', N'secret!', N'Carol García');
GO
