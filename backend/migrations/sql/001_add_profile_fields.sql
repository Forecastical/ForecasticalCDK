-- Add new columns to Users table if they don't exist
DO $$ 
BEGIN 
    -- profile_image column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='Users' AND column_name='profile_image') THEN
        ALTER TABLE "Users" ADD COLUMN profile_image VARCHAR(255);
    END IF;

    -- bio column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='Users' AND column_name='bio') THEN
        ALTER TABLE "Users" ADD COLUMN bio TEXT;
    END IF;

    -- preferred_activities column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='Users' AND column_name='preferred_activities') THEN
        ALTER TABLE "Users" ADD COLUMN preferred_activities TEXT;
    END IF;

    -- favorite_weather column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='Users' AND column_name='favorite_weather') THEN
        ALTER TABLE "Users" ADD COLUMN favorite_weather VARCHAR(50);
    END IF;

    -- notification_email column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='Users' AND column_name='notification_email') THEN
        ALTER TABLE "Users" ADD COLUMN notification_email VARCHAR(255);
    END IF;

    -- theme_preference column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='Users' AND column_name='theme_preference') THEN
        ALTER TABLE "Users" ADD COLUMN theme_preference VARCHAR(20) DEFAULT 'dark';
    END IF;
END $$;