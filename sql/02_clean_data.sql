-- 02_clean_data.sql
-- Purpose:
-- Clean and standardize the raw ecommerce cosmetics dataset.
--
-- Input table:
-- dbo.ecommerce_cosmetics_raw
--
-- Output table:
-- dbo.ecommerce_cosmetics_clean
--
-- Cleaning steps:
-- 1. Remove extra spaces
-- 2. Convert empty strings to NULL
-- 3. Convert price, rating, and no_of_ratings to numeric values
-- 4. Rename columns into cleaner analytical names
-- 5. Remove duplicate rows

IF OBJECT_ID('dbo.ecommerce_cosmetics_clean', 'U') IS NOT NULL
    DROP TABLE dbo.ecommerce_cosmetics_clean;
GO

WITH cleaned_raw AS (
    SELECT
        NULLIF(TRIM(product_name), '') AS product_name,
        NULLIF(TRIM(website), '') AS website,
        NULLIF(TRIM(country), '') AS country,
        NULLIF(TRIM(category), '') AS category,
        NULLIF(TRIM(subcategory), '') AS subcategory,
        NULLIF(TRIM(title_href), '') AS title_href,
        NULLIF(TRIM(brand), '') AS brand,
        NULLIF(TRIM(ingredients), '') AS ingredients,
        NULLIF(TRIM(form), '') AS form,
        NULLIF(TRIM(product_type), '') AS product_type,
        NULLIF(TRIM(color), '') AS color,
        NULLIF(TRIM(product_size), '') AS product_size,

        TRY_CONVERT(
            DECIMAL(10,2),
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(TRIM(price), '$', ''),
                    '€', ''),
                '₹', ''),
            ',', '')
        ) AS price,

        TRY_CONVERT(DECIMAL(3,2), TRIM(rating)) AS rating,

        TRY_CONVERT(
            INT,
            REPLACE(TRIM(no_of_ratings), ',', '')
        ) AS no_of_ratings

    FROM dbo.ecommerce_cosmetics_raw
)

SELECT DISTINCT
    product_name,
    website,
    country,
    category,
    subcategory,
    title_href,
    price,
    brand,
    ingredients,
    form,
    product_type,
    color,
    product_size,
    rating,
    no_of_ratings
INTO dbo.ecommerce_cosmetics_clean
FROM cleaned_raw
WHERE product_name IS NOT NULL;
GO
