-- Example SQL queries after loading a CSV table named launches.
SELECT COUNT(*) AS total_launches FROM launches;
SELECT * FROM launches LIMIT 10;
-- Update the column name to match your dataset:
-- SELECT Launch_Site, COUNT(*) AS launch_count
-- FROM launches GROUP BY Launch_Site ORDER BY launch_count DESC;
