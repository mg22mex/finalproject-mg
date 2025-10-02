-- Add Google Drive integration fields to vehicles table
ALTER TABLE vehicles ADD COLUMN IF NOT EXISTS drive_folder_id VARCHAR(255);
ALTER TABLE vehicles ADD COLUMN IF NOT EXISTS drive_folder_url TEXT;
ALTER TABLE vehicles ADD COLUMN IF NOT EXISTS photos_synced BOOLEAN DEFAULT FALSE;

-- Add Drive file tracking to photos table
ALTER TABLE photos ADD COLUMN IF NOT EXISTS drive_file_id VARCHAR(255);
ALTER TABLE photos ADD COLUMN IF NOT EXISTS drive_url TEXT;

-- Create index for Drive folder lookups
CREATE INDEX IF NOT EXISTS idx_vehicles_drive_folder_id ON vehicles(drive_folder_id);
CREATE INDEX IF NOT EXISTS idx_photos_drive_file_id ON photos(drive_file_id);

-- Create Drive files tracking table
CREATE TABLE IF NOT EXISTS drive_files (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
    drive_file_id VARCHAR(255) UNIQUE NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    download_url TEXT,
    synced BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for Drive files
CREATE INDEX IF NOT EXISTS idx_drive_files_vehicle_id ON drive_files(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_drive_files_drive_file_id ON drive_files(drive_file_id);
CREATE INDEX IF NOT EXISTS idx_drive_files_synced ON drive_files(synced);

-- Add comments for documentation
COMMENT ON COLUMN vehicles.drive_folder_id IS 'Google Drive folder ID for vehicle photos';
COMMENT ON COLUMN vehicles.drive_folder_url IS 'Google Drive folder shareable URL';
COMMENT ON COLUMN vehicles.photos_synced IS 'Whether photos have been synced from Drive';
COMMENT ON COLUMN photos.drive_file_id IS 'Google Drive file ID for the photo';
COMMENT ON COLUMN photos.drive_url IS 'Google Drive file shareable URL';
