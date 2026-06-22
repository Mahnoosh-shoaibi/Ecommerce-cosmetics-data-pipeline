-- 01_create_raw_table.sql
-- Purpose:
-- Create a raw SQL table for the original ecommerce cosmetics CSV dataset.
--
-- Source file:
-- data/raw/E-commerce cosmetic dataset.csv
--
-- Notes:
-- This is a RAW table, so all columns are stored as NVARCHAR first.
-- Data type conversion and cleaning will be done later in 02_clean_data.sql.
--
-- Some original CSV column names were renamed for SQL compatibility:
-- title-href   -> title_href
-- size         -> product_size
-- type         -> product_type
-- noofratings  -> no_of_ratings

IF OBJECT_ID('dbo.ecommerce_cosmetics_raw', 'U') IS NOT NULL
    DROP TABLE dbo.ecommerce_cosmetics_raw;
GO

CREATE TABLE dbo.ecommerce_cosmetics_raw (
    product_name    NVARCHAR(255),
    website         NVARCHAR(255),
    country         NVARCHAR(100),
    category        NVARCHAR(100),
    subcategory     NVARCHAR(100),
    title_href      NVARCHAR(1000),
    price           NVARCHAR(50),
    brand           NVARCHAR(255),
    ingredients     NVARCHAR(MAX),
    form            NVARCHAR(100),
    product_type    NVARCHAR(100),
    color           NVARCHAR(100),
    product_size    NVARCHAR(100),
    rating          NVARCHAR(50),
    no_of_ratings   NVARCHAR(50)
);
GO
