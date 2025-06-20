select * from events;
select * from event_types;
select * from event_images;
select * from event_distances;
select * from users;

delete from events;

drop index idx_event_distances_event_id;
drop index idx_event_images_event_id;
drop index idx_events_event_type_id;

drop table event_types CASCADE;;
drop table event_images;
drop table event_distances;
drop table users;
drop table events;


CREATE TABLE IF NOT EXISTS public.events
(
    id serial NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(1000) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    city character varying(100) NOT NULL,
    province character varying(100) NOT NULL,
    event_website character varying(1000),
    organizer character varying(100) NOT NULL,
    active boolean NOT NULL DEFAULT true,
    map_link character varying(1000),
    event_type_id integer NOT NULL,
    multi_day boolean NOT NULL DEFAULT false,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.event_types
(
    id serial NOT NULL,
    type character varying(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.event_images
(
    id serial NOT NULL,
    event_id integer NOT NULL,
    headline boolean NOT NULL DEFAULT false,
    url character varying(1000) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.event_distances
(
    id serial NOT NULL,
    event_id integer NOT NULL,
    day integer NOT NULL,
    distance integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    id serial NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    google_id bigint,
    create_date timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    role character varying(100) NOT NULL,
    password character varying(255) NOT NULL DEFAULT '$2b$12$5VKzhpKhlLPYVW1yHy9w5O7BPJmQ2hLMZtY45BkAvQJt7F4ixU4ca',
    PRIMARY KEY (id),
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.favorite_event
(
    id serial NOT NULL,
    user_id integer NOT NULL,
    event_id integer NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (user_id, event_id)
);

ALTER TABLE IF EXISTS public.events
    ADD FOREIGN KEY (event_type_id)
    REFERENCES public.event_types (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.event_images
    ADD FOREIGN KEY (event_id)
    REFERENCES public.events (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.event_distances
    ADD FOREIGN KEY (event_id)
    REFERENCES public.events (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.favorite_event
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.favorite_event
    ADD FOREIGN KEY (event_id)
    REFERENCES public.events (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

----------------------------------------
-- Create the trigger function
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_date = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger on the users table
CREATE TRIGGER set_update_timestamp
BEFORE UPDATE ON public.users
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- index
CREATE INDEX idx_events_event_type_id ON public.events(event_type_id);
CREATE INDEX idx_event_images_event_id ON public.event_images(event_id);
CREATE INDEX idx_event_distances_event_id ON public.event_distances(event_id);
----------------------------------------


------------------------------------------------------------
--seeding

-- Seed event_types
INSERT INTO public.event_types (type) VALUES
('Marathon'),
('Triathlon'),
('Cycling'),
('Trail Run'),
('Charity Walk');

-- Seed users
INSERT INTO public.users (first_name, last_name, email, google_id, role) VALUES
('Alice', 'Smith', 'alice@example.com', NULL, 'user'),
('Bob', 'Johnson', 'bob@example.com', NULL, 'admin'),
('Carol', 'Williams', 'carol@example.com', NULL, 'user'),
('David', 'Brown', 'david@example.com', NULL, 'user'),
('Eva', 'Jones', 'eva@example.com', NULL, 'user'),
('Frank', 'Garcia', 'frank@example.com', NULL, 'user'),
('Grace', 'Martinez', 'grace@example.com', NULL, 'admin'),
('Henry', 'Davis', 'henry@example.com', NULL, 'user'),
('Isabel', 'Lopez', 'isabel@example.com', NULL, 'user'),
('Jack', 'Wilson', 'jack@example.com', NULL, 'user');

-- Seed events (event_type_id from 1 to 5)
INSERT INTO public.events (
    name, description, start_date, end_date, city, province,
    event_website, organizer, event_type_id, multi_day
) VALUES
('Cape Town Marathon', 'Annual city marathon.', '2025-10-05', '2025-10-05', 'Cape Town', 'Western Cape', 'https://capetownmarathon.com', 'Cape Town Athletics', 1, false),
('Durban Triathlon', 'Swim, cycle, and run on the coast.', '2025-09-12', '2025-09-13', 'Durban', 'KwaZulu-Natal', 'https://durbantri.co.za', 'TriEvents SA', 2, true),
('Jozi Cycle Classic', 'Urban cycling race through Johannesburg.', '2025-08-20', '2025-08-20', 'Johannesburg', 'Gauteng', NULL, 'Cycle Jozi', 3, false),
('Drakensberg Trail Run', 'Scenic trail run in the mountains.', '2025-07-01', '2025-07-02', 'Drakensberg', 'KwaZulu-Natal', 'https://draktrail.com', 'Nature Trails SA', 4, true),
('Mandela Charity Walk', 'Annual walk to raise funds.', '2025-09-01', '2025-09-01', 'Pretoria', 'Gauteng', NULL, 'Mandela Foundation', 5, false),
('Soweto Marathon', 'Run through the historic townships.', '2025-11-03', '2025-11-03', 'Soweto', 'Gauteng', NULL, 'Soweto Runners', 1, false),
('Garden Route Tri', 'Endurance event along the coast.', '2025-12-14', '2025-12-15', 'George', 'Western Cape', NULL, 'GR Events', 2, true),
('Cape Cycle Tour', 'Scenic coastal cycle race.', '2025-03-10', '2025-03-10', 'Cape Town', 'Western Cape', 'https://capecycle.co.za', 'Cape Cycling Club', 3, false),
('Kruger Trail Challenge', 'Adventure running in the bush.', '2025-06-10', '2025-06-11', 'Kruger Park', 'Limpopo', NULL, 'Kruger Adventures', 4, true),
('Charity Fun Walk', 'Community event to raise funds.', '2025-04-01', '2025-04-01', 'Port Elizabeth', 'Eastern Cape', NULL, 'Hope Foundation', 5, false);

-- Seed event_images
INSERT INTO public.event_images (event_id, headline, url) VALUES
(1, true, 'https://example.com/img/capetown.jpg'),
(2, true, 'https://example.com/img/durban.jpg'),
(3, false, 'https://example.com/img/jozi.jpg'),
(4, true, 'https://example.com/img/drakensberg.jpg'),
(5, false, 'https://example.com/img/mandela.jpg'),
(6, true, 'https://example.com/img/soweto.jpg'),
(7, false, 'https://example.com/img/gardenroute.jpg'),
(8, true, 'https://example.com/img/capecycle.jpg'),
(9, false, 'https://example.com/img/kruger.jpg'),
(10, true, 'https://example.com/img/charity.jpg');

-- Seed event_distances (1 per event)
INSERT INTO public.event_distances (event_id, day, distance) VALUES
(1, 1, 42),
(2, 1, 51),
(2, 2, 30),
(3, 1, 20),
(4, 1, 18),
(4, 2, 12),
(5, 1, 5),
(6, 1, 42),
(7, 1, 40),
(7, 2, 30);

-- Seed data
INSERT INTO public.favorite_event (user_id, event_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 3),
(3, 2),
(3, 4),
(4, 1),
(4, 5),
(5, 3),
(5, 4);

------------------------------------------------------------