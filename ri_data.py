class mainshock:
    def __init__(self, name, latitude, longitude, mag, time):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.mag = mag
        self.time = time

ri_mainshocks = [
        mainshock(name = "Lubang, Occidental Mindoro", 
              latitude = "14.05",
              longitude = "119.11",
              mag = "6.4",
              time = "2022-03-14T05:05:48"),

        mainshock(name = "Itbayat, Batanes", 
              latitude = "23.43",
              longitude = "121.57",
              mag = "6.7",
              time = "2022-03-23T01:41:00"),

        mainshock(name = "Tayum, Abra", 
              latitude = "17.63",
              longitude = "120.63",
              mag = "7.0",
              time = "2022-07-27T08:43:24"),

        mainshock(name = "Lagayan, Abra", 
              latitude = "17.77",
              longitude = "120.72",
              mag = "6.4",
              time = "2022-10-25T22:59:02"),

        mainshock(name = "Balut Island, Davao Occidental", 
              latitude = "2.86",
              longitude = "127.04",
              mag = "7.0",
              time = "2023-01-18T14:06:10"),

        mainshock(name = "Sarangani Island, Davao Occidental", 
              latitude = "3.18",
              longitude = "128.13",
              mag = "6.4",
              time = "2023-02-24T04:02:47"),

        mainshock(name = "Sarangani Island, Davao Occidental", 
              latitude = "5.38",
              longitude = "125.24",
              mag = "6.8",
              time = "2023-11-17T16:14:08"),

        mainshock(name = "Hinatuan, Surigao Del Sur", 
              latitude = "8.44",
              longitude = "126.59",
              mag = "7.4",
              time = "2023-12-02T22:37:05"),

        mainshock(name = "Hinatuan, Surigao Del Sur", 
              latitude = "8.49",
              longitude = "126.95",
              mag = "6.6",
              time = "2023-12-03T18:35:50"),

        mainshock(name = "Cagwait, Surigao Del Sur", 
              latitude = "8.96",
              longitude = "126.91",
              mag = "6.8",
              time = "2023-12-04T03:49:33")]
