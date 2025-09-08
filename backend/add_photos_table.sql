-- Add photos table to autosell_mx database
-- Run this script to create the photos table for photo management

-- Create photos table
CREATE TABLE IF NOT EXISTS photos (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    google_drive_id VARCHAR(255) UNIQUE NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100) NOT NULL,
    google_drive_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    description TEXT,
    is_primary BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    uploaded_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_photos_vehicle_id ON photos(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_photos_google_drive_id ON photos(google_drive_id);
CREATE INDEX IF NOT EXISTS idx_photos_is_primary ON photos(is_primary);
CREATE INDEX IF NOT EXISTS idx_photos_is_active ON photos(is_active);
CREATE INDEX IF NOT EXISTS idx_photos_created_at ON photos(created_at);

-- Add photo_count column to vehicles table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'vehicles' AND column_name = 'photo_count') THEN
        ALTER TABLE vehicles ADD COLUMN photo_count INTEGER DEFAULT 0;
    END IF;
END $$;

-- Create function to update photo count
CREATE OR REPLACE FUNCTION update_vehicle_photo_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE vehicles SET photo_count = photo_count + 1 WHERE id = NEW.vehicle_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE vehicles SET photo_count = GREATEST(0, photo_count - 1) WHERE id = OLD.vehicle_id;
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        IF OLD.vehicle_id != NEW.vehicle_id THEN
            UPDATE vehicles SET photo_count = GREATEST(0, photo_count - 1) WHERE id = OLD.vehicle_id;
            UPDATE vehicles SET photo_count = photo_count + 1 WHERE id = NEW.vehicle_id;
        END IF;
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update photo count
DROP TRIGGER IF EXISTS trigger_update_vehicle_photo_count ON photos;
CREATE TRIGGER trigger_update_vehicle_photo_count
    AFTER INSERT OR UPDATE OR DELETE ON photos
    FOR EACH ROW EXECUTE FUNCTION update_vehicle_photo_count();

-- Create function to ensure only one primary photo per vehicle
CREATE OR REPLACE FUNCTION ensure_single_primary_photo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_primary = TRUE THEN
        -- Unset other primary photos for the same vehicle
        UPDATE photos 
        SET is_primary = FALSE 
        WHERE vehicle_id = NEW.vehicle_id 
        AND id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to ensure single primary photo
DROP TRIGGER IF EXISTS trigger_ensure_single_primary_photo ON photos;
CREATE TRIGGER trigger_ensure_single_primary_photo
    BEFORE INSERT OR UPDATE ON photos
    FOR EACH ROW EXECUTE FUNCTION ensure_single_primary_photo();

-- Update existing vehicles with photo count
UPDATE vehicles 
SET photo_count = (
    SELECT COUNT(*) 
    FROM photos 
    WHERE photos.vehicle_id = vehicles.id 
    AND photos.is_active = TRUE
);

-- Grant permissions to autosell_user
GRANT ALL PRIVILEGES ON TABLE photos TO autosell_user;
GRANT USAGE, SELECT ON SEQUENCE photos_id_seq TO autosell_user;

-- Insert sample photo data for testing (optional)
-- INSERT INTO photos (vehicle_id, google_drive_id, file_name, mime_type, description, uploaded_by)
-- VALUES (1, 'sample_drive_id_1', 'sample_photo_1.jpg', 'image/jpeg', 'Sample photo for testing', 'system');

COMMIT;
