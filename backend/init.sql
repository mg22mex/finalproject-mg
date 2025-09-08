-- Autosell.mx Database Initialization Script
-- PostgreSQL Database Schema for Vehicle Management System

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create custom types
CREATE TYPE vehicle_status AS ENUM ('Disponible', 'FOTOS', 'AUSENTE', 'Apartado', 'Vendido');
CREATE TYPE post_status AS ENUM ('active', 'pending', 'failed', 'removed');
CREATE TYPE platform_type AS ENUM ('facebook', 'instagram', 'twitter', 'whatsapp', 'marketplace');

-- Create tables

-- Vehicles table
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(100) UNIQUE,
    marca VARCHAR(100) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    año INTEGER NOT NULL,
    color VARCHAR(50),
    precio DECIMAL(12,2),
    kilometraje VARCHAR(50),
    estatus vehicle_status DEFAULT 'Disponible',
    ubicacion VARCHAR(100),
    descripcion TEXT,
    caracteristicas JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

-- Photos table
CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    drive_url TEXT,
    drive_file_id VARCHAR(255),
    order_index INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT FALSE,
    file_size BIGINT,
    mime_type VARCHAR(100),
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Status history table
CREATE TABLE status_history (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
    old_status vehicle_status,
    new_status vehicle_status NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100),
    reason TEXT,
    notes TEXT
);

-- Social media posts table
CREATE TABLE social_posts (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
    platform platform_type NOT NULL,
    post_id VARCHAR(255),
    external_post_id VARCHAR(255),
    message TEXT,
    status post_status DEFAULT 'active',
    posted_at TIMESTAMP WITH TIME ZONE,
    removed_at TIMESTAMP WITH TIME ZONE,
    engagement_metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Marketplace listings table
CREATE TABLE marketplace_listings (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
    platform platform_type DEFAULT 'marketplace',
    listing_id VARCHAR(255),
    external_listing_id VARCHAR(255),
    status post_status DEFAULT 'active',
    posted_at TIMESTAMP WITH TIME ZONE,
    removed_at TIMESTAMP WITH TIME ZONE,
    repost_count INTEGER DEFAULT 0,
    last_repost_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users table (for authentication)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- API keys table
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    key_name VARCHAR(100) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    permissions JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP WITH TIME ZONE
);

-- Automation workflows table
CREATE TABLE automation_workflows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    workflow_type VARCHAR(100) NOT NULL,
    n8n_workflow_id VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    schedule_cron VARCHAR(100),
    last_run TIMESTAMP WITH TIME ZONE,
    next_run TIMESTAMP WITH TIME ZONE,
    run_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Workflow execution logs table
CREATE TABLE workflow_executions (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES automation_workflows(id) ON DELETE CASCADE,
    execution_id VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Analytics data table
CREATE TABLE analytics_data (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4),
    metric_unit VARCHAR(50),
    data_date DATE NOT NULL,
    data_hour INTEGER,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Market intelligence table
CREATE TABLE market_intelligence (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    data_type VARCHAR(100) NOT NULL,
    raw_data JSONB,
    processed_data JSONB,
    insights TEXT,
    confidence_score DECIMAL(3,2),
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_vehicles_status ON vehicles(estatus);
CREATE INDEX idx_vehicles_marca_modelo ON vehicles(marca, modelo);
CREATE INDEX idx_vehicles_precio ON vehicles(precio);
CREATE INDEX idx_vehicles_created_at ON vehicles(created_at);
CREATE INDEX idx_vehicles_external_id ON vehicles(external_id);

CREATE INDEX idx_photos_vehicle_id ON photos(vehicle_id);
CREATE INDEX idx_photos_order_index ON photos(vehicle_id, order_index);
CREATE INDEX idx_photos_is_primary ON photos(vehicle_id, is_primary);

CREATE INDEX idx_status_history_vehicle_id ON status_history(vehicle_id);
CREATE INDEX idx_status_history_changed_at ON status_history(changed_at);
CREATE INDEX idx_status_history_new_status ON status_history(new_status);

CREATE INDEX idx_social_posts_vehicle_id ON social_posts(vehicle_id);
CREATE INDEX idx_social_posts_platform ON social_posts(platform);
CREATE INDEX idx_social_posts_status ON social_posts(status);
CREATE INDEX idx_social_posts_posted_at ON social_posts(posted_at);

CREATE INDEX idx_marketplace_listings_vehicle_id ON marketplace_listings(vehicle_id);
CREATE INDEX idx_marketplace_listings_status ON marketplace_listings(status);
CREATE INDEX idx_marketplace_listings_posted_at ON marketplace_listings(posted_at);

CREATE INDEX idx_analytics_data_vehicle_id ON analytics_data(vehicle_id);
CREATE INDEX idx_analytics_data_metric_name ON analytics_data(metric_name);
CREATE INDEX idx_analytics_data_data_date ON analytics_data(data_date);

-- Create full-text search indexes
CREATE INDEX idx_vehicles_search ON vehicles USING gin(to_tsvector('spanish', marca || ' ' || modelo || ' ' || COALESCE(descripcion, '')));

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_vehicles_updated_at BEFORE UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_photos_updated_at BEFORE UPDATE ON photos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_social_posts_updated_at BEFORE UPDATE ON social_posts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_marketplace_listings_updated_at BEFORE UPDATE ON marketplace_listings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_automation_workflows_updated_at BEFORE UPDATE ON automation_workflows FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to update primary photo
CREATE OR REPLACE FUNCTION update_primary_photo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_primary = TRUE THEN
        UPDATE photos SET is_primary = FALSE 
        WHERE vehicle_id = NEW.vehicle_id AND id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_primary_photo_trigger BEFORE INSERT OR UPDATE ON photos FOR EACH ROW EXECUTE FUNCTION update_primary_photo();

-- Insert initial data
INSERT INTO users (username, email, hashed_password, full_name, role) VALUES
('admin', 'admin@autosell.mx', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'System Administrator', 'admin'),
('user', 'user@autosell.mx', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO', 'Regular User', 'user');

-- Insert sample automation workflows
INSERT INTO automation_workflows (name, description, workflow_type, is_active) VALUES
('Daily Vehicle Sync', 'Sync vehicle data from Google Sheets daily', 'google_sheets_sync', true),
('Facebook Marketplace Repost', 'Repost vehicles to Facebook Marketplace daily', 'facebook_marketplace', true),
('Social Media Posting', 'Post new vehicles to social media platforms', 'social_media_posting', true),
('Status Change Handler', 'Handle vehicle status changes automatically', 'status_change_handler', true);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO autosell_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO autosell_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO autosell_user;

-- Create views for common queries
CREATE VIEW vehicle_summary AS
SELECT 
    v.id,
    v.marca,
    v.modelo,
    v.año,
    v.color,
    v.precio,
    v.estatus,
    v.ubicacion,
    v.created_at,
    COUNT(p.id) as photo_count,
    COUNT(s.id) as social_posts_count,
    COUNT(m.id) as marketplace_listings_count
FROM vehicles v
LEFT JOIN photos p ON v.id = p.vehicle_id
LEFT JOIN social_posts s ON v.id = s.vehicle_id AND s.status = 'active'
LEFT JOIN marketplace_listings m ON v.id = m.vehicle_id AND m.status = 'active'
GROUP BY v.id, v.marca, v.modelo, v.año, v.color, v.precio, v.estatus, v.ubicacion, v.created_at;

-- Create view for analytics
CREATE VIEW daily_analytics AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_vehicles,
    COUNT(CASE WHEN estatus = 'Disponible' THEN 1 END) as available_vehicles,
    COUNT(CASE WHEN estatus = 'Vendido' THEN 1 END) as sold_vehicles,
    COUNT(CASE WHEN estatus = 'Apartado' THEN 1 END) as reserved_vehicles,
    AVG(precio) as average_price
FROM vehicles
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Print completion message
DO $$
BEGIN
    RAISE NOTICE 'Autosell.mx database schema created successfully!';
    RAISE NOTICE 'Tables created: vehicles, photos, status_history, social_posts, marketplace_listings, users, api_keys, automation_workflows, workflow_executions, analytics_data, market_intelligence';
    RAISE NOTICE 'Indexes and triggers created for optimal performance';
    RAISE NOTICE 'Sample data inserted for users and automation workflows';
    RAISE NOTICE 'Views created for common queries and analytics';
END $$;
