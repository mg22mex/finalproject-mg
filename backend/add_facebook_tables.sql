-- Facebook Reposting System Tables
-- This script adds the necessary tables for Facebook automation

-- Add social_posts table
CREATE TABLE IF NOT EXISTS social_posts (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    post_id VARCHAR(255),
    external_post_id VARCHAR(255),
    message TEXT,
    status VARCHAR(50) DEFAULT 'active',
    posted_at TIMESTAMP WITH TIME ZONE,
    removed_at TIMESTAMP WITH TIME ZONE,
    engagement_metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add automation_workflows table
CREATE TABLE IF NOT EXISTS automation_workflows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    workflow_type VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    config JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_social_posts_vehicle_id ON social_posts(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_social_posts_platform ON social_posts(platform);
CREATE INDEX IF NOT EXISTS idx_social_posts_status ON social_posts(status);
CREATE INDEX IF NOT EXISTS idx_social_posts_created_at ON social_posts(created_at);
CREATE INDEX IF NOT EXISTS idx_automation_workflows_type ON automation_workflows(workflow_type);
CREATE INDEX IF NOT EXISTS idx_automation_workflows_active ON automation_workflows(is_active);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_social_posts_updated_at 
    BEFORE UPDATE ON social_posts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample automation workflow for Facebook
INSERT INTO automation_workflows (name, workflow_type, is_active, config) VALUES (
    'Facebook Daily Reposting',
    'facebook_reposting',
    false,
    '{
        "is_active": false,
        "time_of_day": "09:00",
        "days_of_week": [1, 2, 3, 4, 5],
        "max_posts_per_day": 5,
        "post_interval_hours": 4,
        "include_marketplace": true
    }'
) ON CONFLICT (workflow_type) DO NOTHING;

-- Add sample social posts for testing
INSERT INTO social_posts (vehicle_id, platform, message, status, posted_at) VALUES 
(1, 'facebook', '🚗 ¡Excelente oportunidad! 2020 Toyota Camry en perfecto estado, solo 45,000 km. Precio especial: $250,000. ¡Llámanos hoy mismo!', 'posted', CURRENT_TIMESTAMP - INTERVAL '2 days'),
(2, 'facebook', '🚗 ¡Excelente oportunidad! 2019 Honda Civic en perfecto estado, solo 38,000 km. Precio especial: $220,000. ¡Llámanos hoy mismo!', 'posted', CURRENT_TIMESTAMP - INTERVAL '1 day'),
(3, 'facebook', '🚗 ¡Excelente oportunidad! 2021 Nissan Sentra en perfecto estado, solo 52,000 km. Precio especial: $280,000. ¡Llámanos hoy mismo!', 'posted', CURRENT_TIMESTAMP - INTERVAL '3 days')
ON CONFLICT DO NOTHING;

-- Grant permissions to autosell_user
GRANT ALL PRIVILEGES ON TABLE social_posts TO autosell_user;
GRANT ALL PRIVILEGES ON TABLE automation_workflows TO autosell_user;
GRANT USAGE, SELECT ON SEQUENCE social_posts_id_seq TO autosell_user;
GRANT USAGE, SELECT ON SEQUENCE automation_workflows_id_seq TO autosell_user;

-- Add comments for documentation
COMMENT ON TABLE social_posts IS 'Stores social media posts for vehicles across different platforms';
COMMENT ON TABLE automation_workflows IS 'Stores automation workflow configurations for various tasks';
COMMENT ON COLUMN social_posts.platform IS 'Social media platform (facebook, instagram, marketplace, etc.)';
COMMENT ON COLUMN social_posts.status IS 'Post status (draft, scheduled, posted, failed, deleted, test)';
COMMENT ON COLUMN automation_workflows.config IS 'JSON configuration for the automation workflow';
