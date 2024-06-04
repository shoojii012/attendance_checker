-- Function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Trigger for devices table
CREATE TRIGGER update_devices_updated_at
BEFORE UPDATE ON devices
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Trigger for logs table
CREATE TRIGGER update_logs_updated_at
BEFORE UPDATE ON logs
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();
