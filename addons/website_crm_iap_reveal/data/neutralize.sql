INSERT INTO ir_config_parameter (key, value)
VALUES ('reveal.endpoint', 'https://iap-services-test.leansoft.vn')
    ON CONFLICT (key) DO
       UPDATE SET value = 'https://iap-services-test.leansoft.vn';
