-- Users Table (No changes needed)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Store hashed password
    email VARCHAR(100) UNIQUE NOT NULL,
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Auctions Table (No changes needed)
CREATE TABLE auctions (
    auction_id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(user_id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(255), -- Optional URL to the item's image
    starting_price DECIMAL(10, 2) NOT NULL,
    current_bid DECIMAL(10, 2),
    bid_count INTEGER DEFAULT 0,
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'ended', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Bids Table (No changes needed)
CREATE TABLE bids (
    bid_id SERIAL PRIMARY KEY,
    auction_id INTEGER NOT NULL REFERENCES auctions(auction_id),
    bidder_id INTEGER NOT NULL REFERENCES users(user_id),
    bid_amount DECIMAL(10, 2) NOT NULL,
    bid_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (auction_id, bidder_id, bid_amount) -- Prevent duplicate bids by the same user for the same amount on the same auction
);

-- Comments Table
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    auction_id INTEGER NOT NULL REFERENCES auctions(auction_id) ON DELETE CASCADE, -- If an auction is deleted, delete its comments
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,    -- If a user is deleted, delete their comments
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Likes Table (Many-to-many relationship between users and auctions)
CREATE TABLE likes (
    like_id SERIAL PRIMARY KEY,
    auction_id INTEGER NOT NULL REFERENCES auctions(auction_id) ON DELETE CASCADE, -- If an auction is deleted, delete its likes
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,       -- If a user is deleted, delete their likes
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (auction_id, user_id) -- Ensure a user can only like an auction once
);

-- Indexes for the new tables (for faster querying)
CREATE INDEX idx_comments_auction_id ON comments (auction_id);
CREATE INDEX idx_comments_user_id ON comments (user_id);
CREATE INDEX idx_likes_auction_id ON likes (auction_id);
CREATE INDEX idx_likes_user_id ON likes (user_id);
CREATE INDEX idx_likes_auction_user ON likes (auction_id, user_id); -- For efficient checking if a user has liked an auction