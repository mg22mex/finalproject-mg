-- Multiple Facebook Accounts Support
-- This script adds support for 3 Facebook accounts with different automation modes

-- Add facebook_accounts table
CREATE TABLE IF NOT EXISTS facebook_accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    account_type VARCHAR(50) NOT NULL DEFAULT 'manual', -- 'manual', 'auto'
    is_active BOOLEAN DEFAULT TRUE,
    access_token VARCHAR(1000),
    page_id VARCHAR(255),
    user_id VARCHAR(255),
    app_id VARCHAR(255),
    app_secret VARCHAR(255),
    automation_config JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add account_id to social_posts table
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS account_id INTEGER REFERENCES facebook_accounts(id);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_social_posts_account_id ON social_posts(account_id);
CREATE INDEX IF NOT EXISTS idx_facebook_accounts_type ON facebook_accounts(account_type);
CREATE INDEX IF NOT EXISTS idx_facebook_accounts_active ON facebook_accounts(is_active);

-- Insert 3 Facebook accounts
INSERT INTO facebook_accounts (name, account_type, automation_config) VALUES 
('Manual Account', 'manual', '{"auto_posting": false, "manual_only": true}'),
('Auto Account 1', 'auto', '{"auto_posting": true, "schedule": {"time": "09:00", "days": [1,2,3,4,5], "max_posts_per_day": 3}}'),
('Auto Account 2', 'auto', '{"auto_posting": true, "schedule": {"time": "14:00", "days": [1,2,3,4,5], "max_posts_per_day": 3}}')
ON CONFLICT DO NOTHING;

-- Update existing social posts to use account_id 1 (Manual Account)
UPDATE social_posts SET account_id = 1 WHERE account_id IS NULL;

-- Add trigger to update updated_at timestamp
CREATE TRIGGER update_facebook_accounts_updated_at 
    BEFORE UPDATE ON facebook_accounts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON TABLE facebook_accounts TO autosell_user;
GRANT USAGE, SELECT ON SEQUENCE facebook_accounts_id_seq TO autosell_user;

-- Add comments
COMMENT ON TABLE facebook_accounts IS 'Stores multiple Facebook account configurations';
COMMENT ON COLUMN facebook_accounts.account_type IS 'Account automation type: manual or auto';
COMMENT ON COLUMN facebook_accounts.automation_config IS 'JSON configuration for automation settings';
