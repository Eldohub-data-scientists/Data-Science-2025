-- ===============================
-- My aata tables
-- ===============================
CREATE TABLE DataDictionary (
    FieldName TEXT PRIMARY KEY,
    Description TEXT
);

CREATE TABLE Metrics (
    MetricName TEXT PRIMARY KEY,
    Description TEXT
);

-- ===============================
-- Geography tables
-- ===============================
CREATE TABLE State (
    RegionID INT PRIMARY KEY,
    StateName TEXT NOT NULL
);

CREATE TABLE County (
    RegionID INT PRIMARY KEY,
    CountyName TEXT NOT NULL,
    StateID INT NOT NULL,
    FOREIGN KEY (StateID) REFERENCES State(RegionID)
);

CREATE TABLE City (
    RegionID INT PRIMARY KEY,
    CityName TEXT NOT NULL,
    CountyID INT NOT NULL,
    FOREIGN KEY (CountyID) REFERENCES County(RegionID)
);

CREATE TABLE Zip (
    RegionID INT PRIMARY KEY,
    ZipCode TEXT NOT NULL,
    CityID INT NOT NULL,
    FOREIGN KEY (CityID) REFERENCES City(RegionID)
);

CREATE TABLE Neighborhood (
    RegionID INT PRIMARY KEY,
    NeighborhoodName TEXT NOT NULL,
    ZipID INT NOT NULL,
    FOREIGN KEY (ZipID) REFERENCES Zip(RegionID)
);

-- ===============================
-- Crosswalk tables
-- ===============================
CREATE TABLE Crosswalk_City (
    RegionID INT NOT NULL,
    CityID INT NOT NULL,
    PRIMARY KEY (RegionID, CityID),
    FOREIGN KEY (CityID) REFERENCES City(RegionID)
);

CREATE TABLE Crosswalk_County (
    RegionID INT NOT NULL,
    CountyID INT NOT NULL,
    PRIMARY KEY (RegionID, CountyID),
    FOREIGN KEY (CountyID) REFERENCES County(RegionID)
);

-- ===============================
-- Time series tables
-- ===============================
CREATE TABLE StateTimeSeries (
    RegionID INT NOT NULL,
    Date DATE NOT NULL,
    MedianValue REAL,
    RentIndex REAL,
    PRIMARY KEY (RegionID, Date),
    FOREIGN KEY (RegionID) REFERENCES State(RegionID)
);

CREATE TABLE CountyTimeSeries (
    RegionID INT NOT NULL,
    Date DATE NOT NULL,
    MedianValue REAL,
    RentIndex REAL,
    PRIMARY KEY (RegionID, Date),
    FOREIGN KEY (RegionID) REFERENCES County(RegionID)
);

CREATE TABLE CityTimeSeries (
    RegionID INT NOT NULL,
    Date DATE NOT NULL,
    MedianValue REAL,
    RentIndex REAL,
    PRIMARY KEY (RegionID, Date),
    FOREIGN KEY (RegionID) REFERENCES City(RegionID)
);

CREATE TABLE MetroTimeSeries (
    RegionID INT NOT NULL,
    Date DATE NOT NULL,
    MedianValue REAL,
    RentIndex REAL,
    PRIMARY KEY (RegionID, Date)
);

CREATE TABLE ZipTimeSeries (
    RegionID INT NOT NULL,
    Date DATE NOT NULL,
    MedianValue REAL,
    RentIndex REAL,
    PRIMARY KEY (RegionID, Date),
    FOREIGN KEY (RegionID) REFERENCES Zip(RegionID)
);

CREATE TABLE NeighborhoodTimeSeries (
    RegionID INT NOT NULL,
    Date DATE NOT NULL,
    MedianValue REAL,
    RentIndex REAL,
    PRIMARY KEY (RegionID, Date),
    FOREIGN KEY (RegionID) REFERENCES Neighborhood(RegionID)
);

-- ===============================
-- CSV Imports 
-- ===============================
\copy DataDictionary FROM '/home/bismark/Downloads/SQL/DataDictionaryclean-csv.csv' CSV HEADER;

\copy Crosswalk_City FROM '/home/bismark/Downloads/SQL/cities_crosswalk_clean.csv..csv' CSV HEADER;

\copy Crosswalk_County FROM '/home/bismark/Downloads/SQL/CountyCrossWalk-Zillowclean-csv.csv' CSV HEADER;

\copy StateTimeSeries FROM '/home/bismark/Downloads/SQL/State_time_series.csv' CSV HEADER;

\copy CountyTimeSeries FROM '/home/bismark/Downloads/SQL/County-time-seriesclean-csv.csv' CSV HEADER;

\copy CityTimeSeries FROM '/home/bismark/Downloads/SQL/city_timeseriesclean.csv.csv' CSV HEADER;

\copy MetroTimeSeries FROM '/home/bismark/Downloads/SQL/Metro-time-series-csvclean.csv' CSV HEADER;

\copy ZipTimeSeries FROM '/home/bismark/Downloads/SQL/Zip_time_series.csv' CSV HEADER;

\copy NeighborhoodTimeSeries FROM '/home/bismark/Downloads/SQL/Neighborhood_time_series.csv' CSV HEADER;
