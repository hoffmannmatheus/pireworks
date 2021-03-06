
--
-- Create database table, if needed.
--
CREATE TABLE IF NOT EXISTS configuration ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    is_default INTEGER DEFAULT 0 NOT NULL,
    name VARCHAR(80) NOT NULL, -- UNIQUE!
	colors TEXT NOT NULL,
	trigger_threshold INTEGER NOT NULL,
	trigger_offset INTEGER NOT NULL,
	scaled_max_value INTEGER NOT NULL,
	output_binary INTEGER NOT NULL,
	chunk INTEGER NOT NULL,
	rate INTEGER NOT NULL
); 

--
-- (Re)Insert default configuration.
--
REPLACE INTO configuration (
	id,
	is_default,
	name,
	colors,
	trigger_threshold,
	trigger_offset,
	scaled_max_value,
	output_binary,
	chunk,
	rate
) VALUES (
	0,  			  	-- id
	1,					-- is_default
	"default",			-- name
	"red,green,blue,teal,purple,aquamarine,indigo",	-- colors, should be comma separated values, in the correct TONE order (C, D, E, F, G, A, B) 
	200000,				-- trigger_threshold
	300, 				-- trigger_offset
	255,				-- scaled_max_value
	1,					-- output_binary
	8192,				-- chunk
	44100				-- rate
);

--
-- TODO: Insert more preset configurations, like 'noisy room' or 'quiet room'
--
