select * from events;
select * from event_types;
select * from event_images;
select * from event_distances;
select * from users;
select * from provinces;

delete from events;

drop index idx_event_distances_event_id;
drop index idx_event_images_event_id;
drop index idx_events_event_type_id;

drop table event_types CASCADE;;
drop table event_images;
drop table event_distances;
drop table favorite_event;
drop table users;
drop table event_event_types_junction;
drop table events;
drop table provinces;


CREATE TABLE IF NOT EXISTS public.events
(
    id serial NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(1000) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    city character varying(100) NOT NULL,
    province character varying(100) NOT NULL,
    province_id integer NOT NULL,
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

CREATE TABLE IF NOT EXISTS public.provinces
(
    id serial NOT NULL,
    name character varying(100) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.event_event_types_junction
(
    event_id integer NOT NULL,
    event_event_types_junction integer NOT NULL,
    PRIMARY KEY (event_id, event_event_types_junction)
);

ALTER TABLE IF EXISTS public.events
    ADD FOREIGN KEY (province_id)
    REFERENCES public.provinces (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


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


ALTER TABLE IF EXISTS public.event_event_types_junction
    ADD FOREIGN KEY (event_id)
    REFERENCES public.events (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.event_event_types_junction
    ADD FOREIGN KEY (event_event_types_junction)
    REFERENCES public.event_types (id) MATCH SIMPLE
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
('XCO'),
('Marathon/Half-marathon'),
('Ultra-marathon'),
('Stage Race'),
('Gravel'),
('24-Hour'),
('Ultra-endurance'),
('Enduro'),
('Downhill');

INSERT INTO public.provinces (name) VALUES
('Free State'),
('Gauteng'),
('KwaZulu-Natal'),
('Limpopo'),
('Mpumalanga'),
('Northern Cape'),
('North West'),
('Western Cape'),
('Eastern Cape');
------------------------------------------------------------